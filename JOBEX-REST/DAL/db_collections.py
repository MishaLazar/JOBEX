
class DbCollections:

    collection_names = {
        "engagements_collection": "engagements",
        "positions_col": "positions",
        "users_col": "users",
        "token_blacklist_collection": "token_blacklist",
        "skills": "skills",
        "student_skills": "student_skills",
        "match": "match",
        "position_skills": "position_skills",
        "jobs": "jobs"
    }

    @staticmethod
    def get_collection(key):
        return DbCollections.collection_names[key]

    @staticmethod
    def get_position_collection():
        return DbCollections.collection_names['positions_col']

    @staticmethod
    def get_student_collection():
        return DbCollections.collection_names['users_col']

    @staticmethod
    def get_position_skills_collection():
        return DbCollections.collection_names['position_skills']

    @staticmethod
    def get_student_skills_collection():
        return DbCollections.collection_names['student_skills']

    @staticmethod
    def get_skills_collection():
        return DbCollections.collection_names['skills']

    @staticmethod
    def get_job_collection():
        return DbCollections.collection_names['jobs']

    @staticmethod
    def get_match_collectio():
        return DbCollections.collection_names['match']