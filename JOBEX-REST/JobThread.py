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
from Utils.Logger import  Logger

config = ConfigHelper.get_instance()
log = Logger(name='Job').logger

CONST_USE_SAVED_PICKLE = config.read_sentiment(Key='CONST_USE_SAVED_PICKLE')
CATEGORY = 0.2
SUB_CATEGORY = 0.3
SKILLS = 0.3
OTHERS = 0.2

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
    save_classifier = open("tweetposneg.pickle","wb")
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

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            self.do_job()

            time.sleep(self.interval)

    def do_job(self):
        log.debug('do_job')
        jobs = self.get_jobs()
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

                    log.debug('rematch by student_id :' + _job.source_objectid)
                    student_skills = self.on_get_student_skills(_job.source_objectid, all_students_skills)
                    if student_skills is not None:
                        s_categories = []
                        s_sub_categories = []
                        s_skills = []
                        for ss in student_skills:
                            if not ss['category_id'] in s_categories:
                                s_categories.append(ss['category_id'])
                            if not ss['sub_category_id'] in s_sub_categories:
                                s_sub_categories.append(ss['sub_category_id'])
                            for s in ss['skills']:
                                if not s['skill_Id'] in s_skills:
                                    s_skills.append(s['skill_Id'])

                        p_categories = []
                        p_sub_categories = []
                        p_skills = []
                        for position in all_active_positions:
                            position_skills = self.get_positions_skill_list_by_position_id(str(position['_id']),
                                                                                           all_positions_skills)
                            if position_skills is not None:
                                log.debug('job working on position:' + position['position_name'])
                                for ps in position_skills:
                                    if not ps['category_id'] in p_categories:
                                        p_categories.append(ps['category_id'])
                                    if not ps['sub_category_id'] in p_sub_categories:
                                        p_sub_categories.append(ps['sub_category_id'])
                                    for s in ps['skills']:
                                        if not s['skill_Id'] in p_skills:
                                            p_skills.append(s['skill_Id'])
                                if p_categories.__len__() > 0:
                                    category_similarity = self.calculate_similarity(s_categories, p_categories)
                                    sub_categories_similarity = self.calculate_similarity(s_sub_categories,
                                                                                          p_sub_categories)
                                    skill_similarity = self.calculate_similarity(s_skills, p_skills)
                                    match = Match(_job.source_objectid, str(position['_id']),
                                                  self.calculate_match_level(category_similarity,
                                                                             sub_categories_similarity,
                                                                             skill_similarity))
                                    if match.match_level_id > ConfigHelper.read_app_settings('MinMatchLevel'):
                                        matches.append(match)
                elif int(_job.job_type_id) == 2:  # rematch by position
                    log.debug('rematch by position :' + _job.source_objectid)
                    position_skills = self.get_positions_skill_list_by_position_id(_job.source_objectid,
                                                                                   all_positions_skills)
                    p_categories = []
                    p_sub_categories = []
                    p_skills = []
                    if position_skills is not None:
                        for ps in position_skills:
                            if not ps['category_id'] in p_categories:
                                p_categories.append(ps['category_id'])
                            if not ps['sub_category_id'] in p_sub_categories:
                                p_sub_categories.append(ps['sub_category_id'])
                            for s in ps['skills']:
                                if not s['skill_Id'] in p_skills:
                                    p_skills.append(s['skill_Id'])
                        for student in all_active_students:
                            log.debug('job working on student:' + student['email'])
                            student_skills = self.on_get_student_skills(str(student['_id']), all_students_skills)
                            if student_skills is not None:
                                s_categories = []
                                s_sub_categories = []
                                s_skills = []
                                for ss in student_skills:
                                    if not ss['category_id'] in s_categories:
                                        s_categories.append(ss['category_id'])
                                    if not ss['sub_category_id'] in s_sub_categories:
                                        s_sub_categories.append(ss['sub_category_id'])
                                    for s in ss['skills']:
                                        if not s['skill_Id'] in s_skills:
                                            s_skills.append(s['skill_Id'])
                                if s_categories.__len__() > 0:
                                    category_similarity = self.calculate_similarity(s_categories, p_categories)
                                    sub_categories_similarity = self.calculate_similarity(s_sub_categories,
                                                                                          p_sub_categories)
                                    skill_similarity = self.calculate_similarity(s_skills, p_skills)
                                    match = Match(student['_id'], _job.source_objectid,
                                                  self.calculate_match_level(category_similarity,
                                                                             sub_categories_similarity,
                                                                             skill_similarity))
                                    if match.match_level_id > ConfigHelper.read_app_settings('MinMatchLevel'):
                                        matches.append(match)
                elif int(_job.job_type_id) == 3:  # Sentiment analysis
                    log.debug('start sentiment analysis job for object_id:' + _job.source_objectid)
                    txt_to_evaluate = self.get_text_to_analise(_job.source_objectid)
                    valued = classifier.classify(extract_features(txt_to_evaluate.split()))
                    lineLen = len(txt_to_evaluate.split())
                    ss = sid.polarity_scores(txt_to_evaluate)
                    for k in ss:
                        if (k != 'compound' and k != 'pos'):
                            log.debug("{0}: {1}, ".format(k, ss[k]))
                        if (k == 'pos'):
                            log.debug("{0}: {1} ".format(k, ss[k]))
                log.debug('finished working on job_id: ' + _job.job_id)
                self.on_job_finish(job=_job, status=1)
            except IOError:
                log.error('failed to working on job_id: ' + _job.job_id)
                self.on_job_finish(job=_job, status=-1)
        for m in matches:
            log.debug('student:' + str(m.student_id) + ' psition: ' + str(m.position_id) + ' match_level')
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
            "active": "Yes"
        }
        return db_client.get_many_docs_from_collection(DbCollections.get_position_collection(), query)

    def get_all_active_students(self):
        db_client = Client()
        query = {
            "UserTypeId": 1,
            "status": 1
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
            if ss['student_id'] == _id:
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
            if ps['position_id'] == position_id:
                return ps['position_skill_list']

        return None

    def get_all_students_skills(self):
        db_client = Client()
        return db_client.find_by_collection(DbCollections.get_student_skills_collection())

    def calculate_similarity(self, s_skills, p_skills):
        return Similarity.jaccard_similarity(s_skills, p_skills)

    def calculate_match_level(self, category_similarity, sub_categories_similarity, skill_similarity):
        return (category_similarity * CATEGORY) + \
               (sub_categories_similarity * SUB_CATEGORY) + \
               (skill_similarity * SKILLS) + \
               (OTHERS * 1)
        #TODO:// Comapny grade

    def save_match(self, match):
        db_client = Client()
        filter_json = {
            "student_id": match.student_id,
            "position_id": match.position_id
        }
        je = JSONEncoder()
        doc_json = {
            '$set': {
                "student_id": match.student_id,
                "position_id": match.position_id,
                "match_level_id": match.match_level_id,
                "match_update_date": match.match_update_date,
                "is_deleted": match.is_deleted
            }
        }
        result = db_client.update_single_doc_in_collection(DbCollections.get_match_collectio(),
                                                           filter_json, doc_json,
                                                           update_if_exists=True)

        if result is not None:
            log.debug("save_match: " + str(json.dumps(result)))
            return result
        else:
            log.error("failled to save match: " + str(je.default(match.__dict__)))

    def get_text_to_analise(self, source_objectid):
        return 'good job'
