import json
import threading
import time
import logging
from bson import ObjectId
from Classes.job import Job
from Classes.match import Match
from Utils.config_helper import ConfigHelper
from DAL.mongo_db_handler import Client
from DAL.db_collections import DbCollections
from Utils.json_util import JSONEncoder
from Utils.similarity import Similarity

config = ConfigHelper.get_instance()
CATEGORY = 0.2
SUB_CATEGORY = 0.3
SKILLS = 0.3
OTHERS = 0.2

class JobThread(threading.Thread):
    def __init__(self):
        super(JobThread, self).__init__()
        self.daemon = True  # Allow main to exit even if still running.
        self.paused = True  # Start out paused.
        self.state = threading.Condition()

        self.logger = logging.getLogger(name='JOB_THREAD')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(config.read_logger('LOG_PATH'),mode='a', encoding=None, delay=False)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def run(self):
        self.resume()
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            # Do stuff.
            self.do_job()
            time.sleep(10)

    def resume(self):
        self.logger.info('Job Service - resumed')
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

    def pause(self):
        self.logger.info('Job Service - paused')
        with self.state:
            self.paused = True  # Block self.

    def do_job(self):
        self.logger.debug('do_job')
        jobs = self.get_jobs()
        self.logger.debug('getting all active positions')
        all_active_positions = self.get_all_active_positions()
        self.logger.debug('getting all active student profiles')
        all_active_students =  self.get_all_active_students()
        self.logger.debug('getting all students skills')
        all_students_skills = self.get_all_students_skills()
        self.logger.debug('getting all positions_skills')
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
                self.logger.debug('job working on:' + _job.job_id)
                if int(_job.job_type_id) == 1:  # rematch by student

                    self.logger.debug('rematch by student_id :' + _job.source_objectid)
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
                                self.logger.debug('job working on position:' + position['position_name'])
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
                                    sub_categories_similarity = self.calculate_similarity(s_sub_categories, p_sub_categories)
                                    skill_similarity = self.calculate_similarity(s_skills, p_skills)
                                    match = Match(_job.source_objectid,str(position['_id']),
                                                  self.calculate_match_level(category_similarity,
                                                                             sub_categories_similarity,
                                                                             skill_similarity))
                                    matches.append(match)
                elif int(_job.job_type_id) == 2:  # rematch by position
                    self.logger.debug('rematch by position :' + _job.source_objectid)
                    position_skills = self.get_positions_skill_list_by_position_id(_job.source_objectid,
                                                                                   all_positions_skills)
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
                            self.logger.debug('job working on student:' + student['email'])
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
                                    match = Match(student['_id'], _job.source_objectid,self.calculate_match_level(category_similarity,
                                                                                                                   sub_categories_similarity,
                                                                                                                   skill_similarity))
                                    matches.append(match)
                self.logger.debug('finished working on job_id: ' + _job.job_id)
                self.on_job_finish(job=_job, status=0)
            except IOError:
                self.logger.error('failed to working on job_id: ' + _job.job_id)
                self.on_job_finish(job=_job, status=-1)
        for m in matches:
            self.logger.debug('student:' + m.student_id + ' psition: ' + m.position_id + ' match_level')
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
            "status":1
        }
        return db_client.get_many_docs_from_collection(DbCollections.get_student_collection(), query)

    def on_job_finish(self, job, status):
        db_client = Client()
        filter_json = {"_id": ObjectId(job.job_id)}
        doc_json = {'$set': {'status': status}}

        return db_client.update_single_doc_in_collection(DbCollections.get_collection('jobs'),
                                                         filter_json=filter_json, doc_update_json=doc_json)

    def on_get_student_skills(self,_id, all_student_skills):
        for ss in all_student_skills:
            if ss['student_id'] == _id:
                return ss['student_skill_list']

    def on_get_position_skills(self, _id):
        db_client = Client()
        query = {
            "position_id": _id
        }
        return db_client.get_many_docs_from_collection(DbCollections.get_position_skills_collection(), query)

    def update_match_level(self,student_id, position_id, match_level):
        db_client = Client()
        query = {
            "position_id": position_id,
            "student_id": student_id
        }
        match = db_client.get_many_docs_from_collection(DbCollections.get_match_collectio(),json_query=query)

    def get_all_positions_skills(self):
        db_client = Client()
        return db_client.find_by_collection(DbCollections.get_position_skills_collection())

    def get_positions_skill_list_by_position_id(self,position_id,positions_skills_list):
        for ps in positions_skills_list:
            if ps['position_id'] == position_id:
                return ps['position_skill_list']

        return None

    def get_all_students_skills(self):
        db_client = Client()
        return db_client.find_by_collection(DbCollections.get_student_skills_collection())

    def calculate_similarity(self, s_skills, p_skills):
        return Similarity.jaccard_similarity(s_skills,p_skills)

    def calculate_match_level(self, category_similarity, sub_categories_similarity, skill_similarity):
        return (category_similarity * CATEGORY) + \
               (sub_categories_similarity * SUB_CATEGORY) + \
               (skill_similarity * SKILLS) + \
               (OTHERS * 1)




log = logging.getLogger(name='Job - Service')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler(config.read_logger('LOG_PATH'),mode='a', encoding=None, delay=False)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

log.debug('Job service - start')
job = JobThread()
job.run()

