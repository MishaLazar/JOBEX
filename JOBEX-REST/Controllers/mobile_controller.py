from bson import ObjectId
from datetime import datetime
from DAL.mongo_db_handler import Client
from DAL.db_collections import DbCollections


class MobileController:

    # __instance = None

    # @staticmethod
    # def get_instance():
    #     """ Static access method. """
    #     if MobileController.__instance == None:
    #         MobileController()
    #     return MobileController.__instance

    def __init__(self):
        """ Virtually private constructor. """
        # if MobileController.__instance != None:
        #     raise Exception("This class is a singleton!")
        # else:
        #     MobileController.__instance = self

    @staticmethod
    def register_user(new_user):
        db_client = Client()
        new_user_id = db_client.insert_doc_to_collection(collection_name=DbCollections.get_student_collection(),
                                                         doc=new_user)
        if new_user_id:
            return new_user_id
        return None

    # @staticmethod
    # def get_student_engagements(student_id):
    #     db_client = Client()
    #     result = db_client.get_single_doc_from_collection(collection_name=DbCollections.get_collection("users"),
    #                                                       object_id=student_id)
    #     return result

    @staticmethod
    def update_student_profile(student_data):
        db_client = Client()

        query = {
            "_id": ObjectId(student_data['student_id'])
        }
        doc = {
            "$set": {
                "firstName": student_data['Profile']["firstName"],
                "lastName": student_data['Profile']["lastName"],
                "email": student_data['Profile']["email"],
                "address": student_data['Profile']["address"],
                "phone": student_data['Profile']["phone"],
                "birthday": student_data['Profile']["birthday"],
                "location": student_data['Profile']["location"]
            }
        }
        return db_client.update_single_doc_in_collection(DbCollections.get_student_collection(), query, doc,
                                                         True)

    @staticmethod
    def get_student_skills(student_id):
        db_client = Client()
        query = {
            "student_id": student_id
        }
        result = db_client.get_single_doc_from_collection(DbCollections.get_collection("student_skills"),
                                                          json_query=query)
        if result:
            result = result['student_skill_list']
        return result

    @staticmethod
    def set_student_skills(student_id, skills):
        db_client = Client()
        query = {
            "student_id": student_id
        }
        doc = {
            "$set": {"student_skill_list": skills}
        }
        result = db_client.update_single_doc_in_collection(DbCollections.get_student_skills_collection(), query, doc,True)

        if result > 0:
            MobileController.set_student_for_rematch(student_id)

        return result

    @staticmethod
    def set_active_status_on_profile(student_id, active_status):
        db_client = Client()
        if active_status:
            activation_date = datetime.now()

            doc = {
                "$set": {"active": active_status, "activation_date": activation_date}
            }
        else:
            doc = {
                "$set": {"active": active_status}
            }
        doc_filter = {
            "_id": ObjectId(student_id),

        }
        return db_client.update_single_doc_in_collection(DbCollections.get_student_collection(), filter_json=doc_filter,
                                                         doc_update_json=doc)

    @staticmethod
    def set_student_for_rematch(student_id):
        db_client = Client()
        doc = {
            "job_type_id": 1,
            "source_objectid": student_id,
            "creation_date": datetime.now(),
            "status": 0
        }
        return db_client.insert_doc_to_collection(DbCollections.get_job_collection(), doc)

    @staticmethod
    def get_student_engagements(student_id, limit=-1):
        db_client = Client()
        query = {
            "student_id": student_id
        }
        sort_order_param = "creation_date"
        return db_client.get_many_docs_from_collection(DbCollections.get_engagements_collection(), json_query=query,
                                                       sort_order_parameter=sort_order_param, direction=True,
                                                       limit=limit)

    @staticmethod
    def get_student_engagement_by_match(student_id, match_id):
        db_client = Client()
        query = {
            "student_id": student_id,
            "match_id": match_id
        }
        return db_client.get_single_doc_from_collection(DbCollections.get_engagements_collection(), json_query=query)

    @staticmethod
    def get_student_profile(student_id):
        db_client = Client()
        pipeline = [
            {
                "$addFields": {
                    "s_id": {
                        "$toString": "$_id"
                    }

                }
            },
            {
                "$lookup": {
                    "from": "student_skills",
                    "localField": "s_id",
                    "foreignField": "student_id",
                    "as": "student_skills"
                }

            },
            {'$unwind': {'path': '$student_skills', 'preserveNullAndEmptyArrays': True}},
            {
                "$match": {
                    "$and": [{"s_id": student_id}]
                }
            }
            ,
            {
                "$lookup": {
                    "from": "wish_list",
                    "localField": "_id",
                    "foreignField": "student_id",
                    "as": "wish_list"
                }

            },
            {'$unwind': {'path': '$wish_list', 'preserveNullAndEmptyArrays': True}},
            {
                "$project": {
                    "_id": 1,
                    "firstName": 1,
                    "lastName": 1,
                    "email": 1,
                    "username": 1,
                    "password": 1,
                    "userId": 1,
                    "address": 1,
                    "profileImg": 1,
                    "active": 1,
                    "activation_date": 1,
                    "creation_date": 1,
                    "birthday": 1,
                    "phone": 1,
                    "location": 1,
                    'student_skill_list': { '$ifNull' : [ '$student_skills.student_skill_list', [ ] ] },
                    'wish_list': { '$ifNull' : [ '$wish_list.wish_list', [ ] ] }
                }
            }
        ]
        return db_client.get_aggregate_document(DbCollections.get_student_collection(), pipeline=pipeline)

    @staticmethod
    def get_student_engagements2(student_id, limit=100):
        db_client = Client()
        pipeline = [
            {
                "$addFields": {
                    "p_id": {
                        "$toObjectId": "$position_id"

                    }
                }
            }, {
                "$lookup": {
                    "from": "positions",
                    "localField": "p_id",
                    "foreignField": "_id",
                    "as": "positions"
                }

            }, {
                "$unwind": "$positions"
            }, {
                "$lookup": {
                    "from": "companies",
                    "localField": "positions.company_id",
                    "foreignField": "_id",
                    "as": "company"
                }
            }, {
                "$unwind": "$company"
            }, {
                "$match": {
                    "$and": [{"student_id": student_id}]
                }
            }, {
                "$project": {
                    "position_id": 1,
                    "student_id": 1,
                    "match_id": 1,
                    "position_description": "$positions.comment",
                    "position_title": "$positions.position_name",
                    "position_location": "$positions.position_location",
                    "is_new": 1,
                    "status": 1,
                    "is_deleted": 1,
                    "creation_date": 1,
                    "company_name": "$company.name",
                    "company_id": {
                        "$toString": "$company._id"

                    }
                }

            }, {
                "$sort": {
                    "creation_date": 1
                }
            }, {
                "$limit": limit
            }

        ]
        return db_client.get_aggregate_document(DbCollections.get_engagements_collection(), pipeline=pipeline)

    @staticmethod
    def get_student_engagement_by_match2(match_id):
        db_client = Client()
        pipeline = [
            {
                "$addFields": {
                    "p_id": {
                        "$toObjectId": "$position_id"

                    }
                }
            }, {
                "$lookup": {
                    "from": "positions",
                    "localField": "p_id",
                    "foreignField": "_id",
                    "as": "positions"
                }

            }, {
                "$unwind": "$positions"
            },
            {
                "$lookup": {
                    "from": "companies",
                    "localField": "positions.company_id",
                    "foreignField": "_id",
                    "as": "company"
                }

            }, {
                "$unwind": "$company"
            },
            {
                "$lookup": {
                    "from": "position_skills",
                    "localField": "p_id",
                    "foreignField": "position_id",
                    "as": "position_skills"
                }
            }, {
                "$unwind": "$position_skills"
            }, {
                "$match": {
                    "$and": [{"match_id": match_id}]
                }
            }, {
                "$project": {
                    "position_id": 1,
                    "student_id": 1,
                    "match_id": 1,
                    "position_description": "$positions.position_description",
                    "position_title": "$positions.position_name",
                    "position_location": "$positions.position_location",
                    "is_new": 1,
                    "status": 1,
                    "is_deleted": 1,
                    "creation_date": 1,
                    "company_name": "$company.name",
                    "company_id": {
                        "$toString": "$company._id"

                    },
                    "company_rate":{ '$ifNull' : [ '$company.score', 5 ] }
                    ,
                    "company_description": "$company.description",
                    "position_skill_list": "$position_skills.position_skill_list"
                }

            }

        ]
        return db_client.get_aggregate_document(DbCollections.get_engagements_collection(), pipeline=pipeline)

    @staticmethod
    def get_student_engagement_update(student_id, engagement_id, update_fields):
        db_client = Client()
        query = {
            "_id": ObjectId(engagement_id),
            "student_id": student_id
        }
        doc = {
            "$set": update_fields
        }
        return db_client.update_single_doc_in_collection(DbCollections.get_engagements_collection(), filter_json=query,
                                                         doc_update_json=doc)

    @staticmethod
    def get_dashboard_counters_for_main_chart(student_id):
        db_client = Client()
        matches_pipeline = [
            {
                "$match": {
                    "student_id": student_id
                }
            },
            {
                "$group": {
                    "_id": {"month": {"$month": "$match_update_date"}, "day": {"$dayOfMonth": "$match_update_date"},
                            "year": {"$year": "$match_update_date"}},

                    "count": {"$sum": 1}
                }
            }
        ]

        engagements_pipeline = [
            {
                "$match": {
                    "student_id": student_id
                }
            },
            {
                "$group": {
                    "_id": {"month": {"$month": "$creation_date"}, "day": {"$dayOfMonth": "$creation_date"},
                            "year": {"$year": "$creation_date"}},

                    "count": {"$sum": 1}
                }
            }
        ]

        matches_couts = db_client.get_aggregate_document(DbCollections.get_matches_collection(),
                                                         pipeline=matches_pipeline)
        engagements_counts = db_client.get_aggregate_document(DbCollections.get_engagements_collection(),
                                                              pipeline=engagements_pipeline)

        result = {
            "matches_couts": matches_couts if matches_couts else [],
            "engagements_counts": engagements_counts if engagements_counts else []
        }
        return result

    @staticmethod
    def get_position_skills(position_id):
        db_client = Client()
        query = {
            "position_id": ObjectId(position_id)
        }
        result = db_client.get_single_doc_from_collection(DbCollections.get_position_skills_collection(),
                                                          json_query=query)
        if result:
            result = result['position_skill_list']
        return result

    @staticmethod
    def get_position_dataset():
        db_client = Client()
        matches_pipeline = [
            {
                "$lookup": {
                    "from": "position_skills",
                    "localField": "_id",
                    "foreignField": "position_id",
                    "as": "position_skills"
                }
            },
            {
                "$replaceRoot": {"newRoot": {"$mergeObjects": [{"$arrayElemAt": ["$position_skills", 0]}, "$$ROOT"]}}
            }
            ,
            {
                "$project": {
                    "position_name": 1,
                    "position_department": 1,
                    "position_skill_list": 1
                }
            }]
        return db_client.get_aggregate_document(DbCollections.get_position_collection(),
                                                pipeline=matches_pipeline)

    @staticmethod
    def wish_list_save(student_id, wish_list):
        db_client = Client()
        query = {
            "student_id": ObjectId(student_id)
        }
        doc = {
            "$set": {
                "student_id": ObjectId(student_id),
                "wish_list": wish_list}
        }
        return db_client.update_single_doc_in_collection(DbCollections.get_wish_list_collection(), query, doc,
                                                         True)

    @staticmethod
    def get_wish_list(student_id):
        db_client = Client()
        matches_pipeline = [

            {
                "$match": {
                    "student_id": ObjectId(student_id)
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "wish_list": 1

                }
            }

        ]
        result = db_client.get_aggregate_document(DbCollections.get_wish_list_collection(),
                                                  pipeline=matches_pipeline)
        return result[0]["wish_list"] if result[0]["wish_list"] else []

    @staticmethod
    def post_feedback(feedback_text, engagement_id, company_id):
        db_client = Client()
        feedback_obj = {"feedback_text": feedback_text, "engagement_id": engagement_id, "company_id": company_id}

        feedback_id = db_client.insert_doc_to_collection(DbCollections.get_collection("feedbacks"), doc=feedback_obj)
        job_doc = {
            "job_type_id": 3,
            "source_objectid": feedback_id,
            "creation_date": datetime.now(),
            "status": 0
        }

        return db_client.insert_doc_to_collection(DbCollections.get_job_collection(), job_doc)
