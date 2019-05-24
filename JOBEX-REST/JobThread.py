import json
import threading
import time
import nltk
import csv
import pickle
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bson import ObjectId

from Classes.job import Job
from Classes.match import Match
from Utils.config_helper import ConfigHelper
from DAL.mongo_db_handler import Client
from DAL.db_collections import DbCollections
from Utils.json_encoder import JSONEncoder
from Utils.similarity import Similarity
from Utils.Logger import Logger

config = ConfigHelper.get_instance()
log = Logger(name='Job').logger

CONST_USE_SAVED_PICKLE = config.read_sentiment(Key='CONST_USE_SAVED_PICKLE')
CATEGORY = 0.1
SUB_CATEGORY = 0.15
SKILLS = 0.25
OTHERS = 0.1
LOCATION = 0.4
COMPANY_SCORE = 5.0
nltk.downloader.download('vader_lexicon')
pos_tweets = [('I love this car', 'positive'),
              ('This view is amazing', 'positive'),
              ('I feel great this morning', 'positive'),
              ('I am so excited about the concert', 'positive'),
              ('He is my best friend', 'positive'),
              ('Going well', 'positive'),
              ('Thank you', 'positive'),
              ('Hope you are doing well', 'positive'),
              ('I am very happy', 'positive'),
              ('Good for you', 'positive'),
              ('It is all good. I know about it and I accept it.', 'positive'),
              ('This is really good!', 'positive'),
              ('Tomorrow is going to be fun.', 'positive'),
              ('Smiling all around.', 'positive'),
              ('These are great apples today.', 'positive'),
              ('How about them apples? Thomas is a happy boy.', 'positive'),
              ('Thomas is very zen. He is well-mannered.', 'positive')]

neg_tweets = [('I do not like this car', 'negative'),
              ('I hate this World', 'negative'),
              ('This view is horrible', 'negative'),
              ('I feel tired this morning', 'negative'),
              ('I am not looking forward to the concert', 'negative'),
              ('He is my enemy', 'negative'),
              ('I am a bad boy', 'negative'),
              ('This is not good', 'negative'),
              ('I am bothered by this', 'negative'),
              ('I am not connected with this', 'negative'),
              ('Sadistic creep you ass. Die.', 'negative'),
              ('All sorts of crazy and scary as hell.', 'negative'),
              ('Not his emails, no.', 'negative'),
              ('His father is dead. Returned obviously.', 'negative'),
              ('He has a bomb.', 'negative'),
              ('Too fast to be on foot. We cannot catch them.', 'negative')]

# load more traning data
try:
    with open('JOBEX-REST/labeledTrainData.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[1] == "negative":
                neg_tweets.append((row[2], row[1]))
            elif row[1] == "positive":
                pos_tweets.append((row[2], row[1]))

except:
    pass

tweets = []
for (words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))


def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words


def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


word_features = get_word_features(get_words_in_tweets(tweets))
if CONST_USE_SAVED_PICKLE != 1:
    training_set = nltk.classify.apply_features(extract_features, tweets)
    classifier = nltk.NaiveBayesClassifier.train(training_set)

if CONST_USE_SAVED_PICKLE != 1:
    # optional to save your classifier so you can load it elsewhere without having to rebuild training set every time
    save_classifier = open("tweetposneg.pickle", "wb")
    pickle.dump(classifier, save_classifier)
    save_classifier.close()

else:  # optional load from classifier that was saved previously
    classifier_f = open("tweetposneg.pickle", "rb")
    classifier = pickle.load(classifier_f)
    classifier_f.close()

sid = SentimentIntensityAnalyzer()


class JobThread(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.cities = self.get_cities()
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        time.sleep(1)
        thread.start()  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            self.do_job()

            time.sleep(self.interval)

    def do_job(self):
        log.debug('do_job')
        jobs = self.get_jobs()
        if jobs.__len__() > 0:
            log.debug('getting all active positions')
            all_active_positions = self.get_all_active_positions()
            log.debug('getting all active student profiles')
            all_active_students = self.get_all_active_students()
            log.debug('getting all students skills')
            all_students_skills = self.get_all_students_skills()
            log.debug('getting all positions_skills')
            all_positions_skills = self.get_all_positions_skills()

        matches = []
        for j in jobs:
            try:
                json_obj = json.loads(JSONEncoder().encode(j))
                _job = Job(job_id=json_obj['_id'],
                           job_type_id=int(json_obj['job_type_id']),
                           source_objectid=json_obj['source_objectid'],
                           creation_date=json_obj['creation_date'],
                           status=int(json_obj['status']))
                log.debug('job working on:' + _job.job_id)
                if int(_job.job_type_id) == 1:  # rematch by student
                    working = Match(student_id=_job.source_objectid)
                    working_student = self.student_by_id(student_id=_job.source_objectid, students=all_active_students)
                    if working_student:
                        log.debug('rematch by student_id :' + _job.source_objectid)
                        student_skills = self.on_get_student_skills(_job.source_objectid, all_students_skills)
                        if student_skills is not None:
                            working.source_skills = student_skills
                            for position in all_active_positions:
                                position_skills = self.get_positions_skill_list_by_position_id(str(position['_id']),
                                                                                               all_positions_skills)
                                working.position_id = str(position['_id'])
                                working.regard_object_skills = position_skills
                                working.source_location = working_student['location']
                                working.regard_object_location = position['position_location']
                                working.calculate_match(self.cities)

                                if working.match_level_id > float(ConfigHelper.read_app_settings('MinMatchLevel')):
                                    matches.append(working)
                    else:
                        log.debug('rematch by student_id :' + _job.source_objectid + ', student not found')
                elif int(_job.job_type_id) == 2:  # rematch by position
                    working = Match(position_id=_job.source_objectid)
                    working_position = self.position_by_id(position_id=_job.source_objectid,
                                                           positions=all_active_positions)
                    if working_position:
                        log.debug('rematch by position :' + _job.source_objectid)
                        position_skills = self.get_positions_skill_list_by_position_id(_job.source_objectid,
                                                                                       all_positions_skills)
                        if position_skills is not None:
                            working.source_skills = position_skills
                            for student in all_active_students:
                                student_skills = self.on_get_student_skills(str(student['_id']), all_students_skills)

                                working.student_id = str(student['_id'])
                                working.regard_object_skills = student_skills
                                working.source_location = working_position['position_location']
                                working.regard_object_location = student['location']
                                working.calculate_match(self.cities)

                                if working.match_level_id > float(ConfigHelper.read_app_settings('MinMatchLevel')):
                                    matches.append(working)
                    else:
                        log.debug('rematch by position : ' + _job.source_objectid + ", position not found'")
                elif int(_job.job_type_id) == 3:  # Sentiment analysis
                    log.debug('start sentiment analysis job for object_id:' + _job.source_objectid)
                    feedback = self.get_text_to_analise(_job.source_objectid)
                    company_id = feedback['company_id']
                    txt_to_evaluate = feedback['feedback_text']
                    valued = classifier.classify(extract_features(txt_to_evaluate.split()))
                    lineLen = len(txt_to_evaluate.split())
                    ss = sid.polarity_scores(txt_to_evaluate)
                    positive = ss['pos']
                    negative = ss['neg']
                    neutral = ss['neu']
                    compound = ss['compound']

                    company_score = self.get_company_score(company_id)

                    if compound > 0:
                        if positive > 0.6:
                            if company_score < COMPANY_SCORE:
                                p_cs =  company_score / COMPANY_SCORE
                                p_to_accumulate = 1 - p_cs
                                avg_dividend = company_score + p_to_accumulate
                                company_score = (company_score + avg_dividend) / 2
                    elif compound < 0:
                        if negative < 0.5:
                            if company_score > 0:
                                p_cs = company_score / COMPANY_SCORE
                                if p_cs == 1:
                                    p_cs = p_cs - 0.2
                                p_to_accumulate = 1 - p_cs
                                avg_dividend = company_score - p_to_accumulate
                                company_score = (company_score + avg_dividend) / 2

                    self.update_company_score(company_score=company_score, company_id= company_id)

                log.debug('finished working on job_id: ' + _job.job_id)
                self.on_job_finish(job=_job, status=1)
            except IOError:
                log.error('failed to working on job_id: ' + _job.job_id)
                self.on_job_finish(job=_job, status=-1)
        for m in matches:
            log.debug('student:' + str(m.student_id) + ' psition: ' + str(m.position_id) + ' match_level' + str(m.match_level_id))
            self.save_match(m)

    def get_jobs(self):
        db_client = Client()
        query = {
            "status": 0
        }
        return db_client.get_many_docs_from_collection(DbCollections.get_job_collection(), query)

    def get_all_active_positions(self):
        db_client = Client()
        query = {
            "position_active": True
        }
        return db_client.get_many_docs_from_collection(DbCollections.get_position_collection(), query)

    def get_all_active_students(self):
        db_client = Client()
        query = {
            "user_type": "student",
            "active": True
        }
        return db_client.get_many_docs_from_collection(DbCollections.get_student_collection(), query)

    def on_job_finish(self, job, status):
        db_client = Client()
        filter_json = {"_id": ObjectId(job.job_id)}
        doc_json = {'$set': {'status': status}}

        return db_client.update_single_doc_in_collection(DbCollections.get_collection('jobs'),
                                                         filter_json=filter_json, doc_update_json=doc_json)

    def on_get_student_skills(self, _id, all_student_skills):
        for ss in all_student_skills:
            if str(ss['student_id']) == _id:
                return ss['student_skill_list']

    def on_get_position_skills(self, _id):
        db_client = Client()
        query = {
            "position_id": _id
        }
        return db_client.get_many_docs_from_collection(DbCollections.get_position_skills_collection(), query)

    def update_match_level(self, student_id, position_id, match_level):
        db_client = Client()
        query = {
            "position_id": position_id,
            "student_id": student_id
        }
        match = db_client.get_many_docs_from_collection(DbCollections.get_match_collectio(), json_query=query)

    def get_all_positions_skills(self):
        db_client = Client()
        return db_client.find_by_collection(DbCollections.get_position_skills_collection())

    def get_positions_skill_list_by_position_id(self, position_id, positions_skills_list):
        for ps in positions_skills_list:
            if str(ps['position_id']) == position_id:
                return ps['position_skill_list']

        return None

    def get_all_students_skills(self):
        db_client = Client()
        return db_client.find_by_collection(DbCollections.get_student_skills_collection())

    def calculate_similarity(self, set1, set2):
        return Similarity.jaccard_similarity(set1, set2)

    def calculate_match_level(self, category_similarity, sub_categories_similarity, skill_similarity
                              , others=1
                              , location=1):
        return (category_similarity * CATEGORY) + \
               (sub_categories_similarity * SUB_CATEGORY) + \
               (skill_similarity * SKILLS) + \
               (OTHERS * others) + \
               (LOCATION * location)
        # TODO:// Comapny grade

    def save_match(self, match):
        db_client = Client()
        filter_json = {
            "student_id": match.student_id,
            "position_id": match.position_id
        }

        doc_json = {
            '$set': {
                "student_id": match.student_id,
                "position_id": match.position_id,
                "match_level_id": match.match_level_id,
                "match_update_date": match.match_update_date,
                "is_deleted": match.is_deleted,
                "is_engaged": match.is_engaged
            }
        }
        result = db_client.update_single_doc_in_collection(DbCollections.get_matches_collection(),
                                                           filter_json, doc_json,
                                                           update_if_exists=True)

        if result is not None:
            log.debug("save_match: " + str(json.dumps(result)))
            return result
        else:
            log.error("failled to save match: " + str(json.dumps(doc_json)))

    def get_text_to_analise(self, source_objectid):
        db_client = Client()
        query = {
            "_id": ObjectId(source_objectid)
        }
        return db_client.get_single_doc_from_collection(DbCollections.get_feedback(), query)


    def get_cities(self):
        db_client = Client()
        return db_client.find_by_collection(DbCollections.get_cities())

    def get_location_match(self, position_location: str, student_location: int):
        location = 0
        student_location = ""
        for city in self.cities:
            if city["city_id"] == student_location:
                student_location = city['city_desc']
                if str(city['city_desc']).lower() == position_location.lower():
                    location = 1

        if location < 1:
            if self.get_city_base(student_location) == self.get_city_base(position_location):
                location = 0.5

        return location

    def get_city_base(self, city_desv: str):
        for city in self.cities:
            if city['city_desc'] == city_desv:
                return city['city_base_id']
            else:
                return None

    def student_by_id(self, student_id: str, students):
        for student in students:
            if str(student['_id']) == student_id:
                return student

        return None

    def position_by_id(self, position_id: str, positions):
        for position in positions:
            if str(position['_id']) == position_id:
                return position

        return None

    def get_company_score(self, company_id):
        db_client = Client()
        query = {
            "_id": ObjectId(company_id)
        }
        company = db_client.get_single_doc_from_collection(DbCollections.get_company(), query)
        company_score = COMPANY_SCORE
        if 'company_score'  in company:
            company_score = company['company_score']

        return company_score

    def update_company_score(self, company_score, company_id):
        db_client = Client()
        filter_json = {
            "_id": ObjectId(company_id),

        }

        doc_json = {
            '$set': {
                "company_score": company_score
            }
        }
        result = db_client.update_single_doc_in_collection(DbCollections.get_company(),
                                                           filter_json, doc_json,
                                                           update_if_exists=True)

        if result is not None:
            log.debug("update_company_score: " + str(json.dumps(result)))
            return result
        else:
            log.error("failled to update_company_score: " + str(json.dumps(doc_json)))
