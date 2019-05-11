from datetime import datetime

from Utils.similarity import Similarity

CATEGORY = 0.1
SUB_CATEGORY = 0.2
SKILLS = 0.2
OTHERS = 0.1
LOCATION = 0.4

class Match:
    others = None
    location = None
    def __init__(self,student_id=None,
                 position_id=None,
                 match_level_id=0,
                 source_skills=None,
                 regard_object_skills=None,
                 regard_object_location=None,
                 source_location=None,
                 is_deleted=False):
        self.match_level_id = match_level_id
        self.position_id = position_id
        self.student_id = student_id
        self.match_update_date = datetime.now()
        self.is_deleted = is_deleted
        self.source_skills = source_skills
        self.regard_object_skills = regard_object_skills
        self.source_location = source_location,
        self.regard_object_location = regard_object_location


    def calculate_match(self,cities):
        if self.source_skills is not None:
            s_categories = []
            s_sub_categories = []
            s_skills = []
            for ss in self.source_skills:
                if not ss['category_id'] in s_categories:
                    s_categories.append(ss['category_id'])
                if not ss['sub_category_id'] in s_sub_categories:
                    s_sub_categories.append(ss['sub_category_id'])
                for s in ss['skills']:
                    if not s['skill_Id'] in s_skills:
                        s_skills.append(s['skill_Id'])
        if self.regard_object_skills is not None:
            r_categories = []
            r_sub_categories = []
            r_skills = []
            for rs in self.regard_object_skills:
                if not rs['category_id'] in r_categories:
                    r_categories.append(int(rs['category_id']))
                if not rs['sub_category_id'] in r_sub_categories:
                    r_sub_categories.append((rs['sub_category_id']))
                for s in rs['skills']:
                    if not s['skill_Id'] in r_skills:
                        r_skills.append(int(s['skill_Id']))

            if r_categories.__len__() > 0:
                self.category_similarity = self.calculate_similarity(s_categories, r_categories)
                self.sub_categories_similarity = self.calculate_similarity(s_sub_categories,
                                                                      r_sub_categories)
                self.skill_similarity = self.calculate_similarity(s_skills, r_skills)
                self.location = \
                    self.get_location_match(r_location=self.regard_object_location,
                                            s_location=self.source_location, cities=cities)
                self.match_level_id = self.calculate_match_level()


    def calculate_similarity(self, set1, set2):
        return Similarity.jaccard_similarity(set1, set2)


    def get_location_match(self, r_location, s_location,cities):
        location = 0
        source_location = ""
        for city in cities:
            if city["city_id"] == s_location:
                source_location = city['city_desc']
                if str(city['city_desc']).lower() == r_location.lower():
                    location = 1

        if location < 1:
            if self.get_city_base(source_location,cities) == self.get_city_base(r_location,cities):
                location = 0.5

        return location

    def get_city_base(self, city_desv: str,cities):
        for city in cities:
            if city['city_desc'] == city_desv:
                return city['city_base_id']
            else:
                return None

    def calculate_match_level(self):
        if self.others is None:
            self.others = 1
        if self.location is None:
            self.location = 1

        return (self.category_similarity * CATEGORY) + \
               (self.sub_categories_similarity * SUB_CATEGORY) + \
               (self.skill_similarity * SKILLS) + \
               (OTHERS * self.others) + \
               (LOCATION * self.location)
        # TODO:// Comapny grade