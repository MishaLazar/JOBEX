
class DbCollections:
    @staticmethod
    def get_collection(key):
        collection_names = {
            "engagements_collection": "engagements",
            "positions_collection": "positions",
            "users_collection": "users",
            "token_blacklist_collection": "token_blacklist",
            "skills": "skills"
        }
        return collection_names[key]

