import json
import threading
import time
import logging
from bson import ObjectId
from Classes.job import Job
from Utils.config_helper import ConfigHelper
from DAL.mongo_db_handler import Client
from DAL.db_collections import DbCollections
from Utils.json_util import JSONEncoder

config = ConfigHelper.get_instance()


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
        jobs =  self.get_jobs()

        for j in jobs:
            json_obj = json.loads(JSONEncoder().encode(j))
            job = Job(job_id=json_obj['_id'],
                      job_type_id=int(json_obj['job_type_id']),
                      source_objectid=json_obj['source_objectid'],
                      creation_date=json_obj['creation_date'],
                      status=int(json_obj['status']))
            self.logger.debug('job working on:' + job.job_id)
            if int(job.job_type_id) == 1:  # rematch by student
                self.logger.debug('rematch by student_id :' + job.source_objectid)
                students = self.get_all_active_students();
                for student in students:
                    self.logger.debug('job working on student:' + student['email'])
            elif int(job.job_type_id) == 2:  # rematch by position
                self.logger.debug('rematch by position :' + job.source_objectid)
                positions = self.get_all_active_positions();
                for position in positions:
                    self.logger.debug('job working on student:' + position['position_name'])

            self.on_job_finish(job=job,status=1)


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

    def on_get_student_skills(self,_id):
        db_client = Client()
        query = {
            "student_id": _id
        }
        return db_client.get_many_docs_from_collection(DbCollections.get_student_skills_collection(), query)

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


log = logging.getLogger(name='Job - Service')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler(config.read_logger('LOG_PATH'),mode='a', encoding=None, delay=False)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

log.debug('Job service - start')
job = JobThread()
job.run()

