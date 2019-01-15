
class Job:

    def __init__(self, job_id,job_type_id,source_objectid,creation_date,status):
        self.creation_date = creation_date
        self.source_objectid = source_objectid
        self.job_type_id = job_type_id
        self.status = status
        self.job_id = job_id

    