
class DbCollections:

    collection_names = {
        "engagements": "engagements",
        "positions": "positions",
        "users": "users",
        "token_blacklist": "token_blacklist",
        "skills": "skills",
        "student_skills": "student_skills",
        "matches": "matches",
        "position_skills": "position_skills",
        "jobs": "jobs",
        "companies": "companies",
        "token_blacklist_collection":"token_blacklist"
    }

    @staticmethod
    def get_collection(key):
        return DbCollections.collection_names[key]

    @staticmethod
    def get_position_collection():
        return DbCollections.collection_names['positions']

    @staticmethod
    def get_student_collection():
        return DbCollections.collection_names['users']

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
    def get_engagements_collection():
        return DbCollections.collection_names['engagements']

    @staticmethod
    def get_matches_collection():
        return DbCollections.collection_names['matches']
