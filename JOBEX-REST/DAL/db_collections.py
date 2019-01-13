
class DbCollections:
    @staticmethod
    def get_collection(key):
        collection_names = {
            "engagements_collection": "engagements",
            "positions_collection": "positions",
            "users_collection": "users",
            "token_blacklist_collection": "token_blacklist",
            "skills": "skills",
            "student_skills": "student_skills",
            "match": "match",
            "position_skills": "position_skills"
        }
        return collection_names[key]

