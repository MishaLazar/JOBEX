import random
from datetime import datetime
from Utils.similarity import Similarity

CATEGORY = 0.1
SUB_CATEGORY = 0.15
SKILLS = 0.25
OTHERS = 0.1
LOCATION = 0.4


class Match:
    others = None
    location = None

    def __init__(self, student_id=None,
                 position_id=None,
                 match_level_id=0,
                 source_skills=None,
                 regard_object_skills=None,
                 regard_object_location=None,
                 source_location=None,
                 is_deleted=False,
                 is_engaged=False):
        self.match_level_id = match_level_id
        self.position_id = position_id
        self.student_id = student_id
        self.match_update_date = datetime.now()
        self.is_deleted = is_deleted
        self.is_engaged = is_engaged
        self.source_skills = source_skills
        self.regard_object_skills = regard_object_skills
        self.source_location = source_location,
        self.regard_object_location = regard_object_location

    def calculate_match(self, cities):
        if self.source_skills is not None:
            s_categories = []
            s_sub_categories = []
            s_skills = []
            for ss in self.source_skills:
                if not ss['category_id'] in s_categories:
                    s_categories.append(int(ss['category_id']))
                if not ss['sub_category_id'] in s_sub_categories:
                    s_sub_categories.append(int(ss['sub_category_id']))
                for s in ss['skills']:
                    if not s['skill_Id'] in s_skills:
                        s_skills.append(int(s['skill_Id']))
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
                self.category_similarity = Match.calculate_similarity(s_categories, r_categories)
                self.sub_categories_similarity = Match.calculate_similarity(s_sub_categories,
                                                                            r_sub_categories)
                self.skill_similarity = Match.calculate_similarity(s_skills, r_skills)
                self.location = \
                    self.get_location_match(r_location=self.regard_object_location,
                                            s_location=self.source_location, cities=cities)
                self.match_level_id = self.calculate_match_level()

    @staticmethod
    def calculate_similarity(set1, set2):
        return Similarity.jaccard_similarity(set1, set2)

    @staticmethod
    def get_location_match(r_location, s_location, cities):
        location = 0
        source_location = ""
        for city in cities:
            if city["city_id"] == s_location:
                source_location = city['city_desc']
                if str(city['city_desc']).lower() == r_location.lower():
                    location = 1

        if location < 1:
            if Match.get_city_base(source_location, cities) == Match.get_city_base(r_location, cities):
                location = 0.5

        return location

    @staticmethod
    def get_city_base(city_desc: str, cities):
        for city in cities:
            if city['city_desc'] == city_desc:
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
        # TODO:// Company grade

    @staticmethod
    def wl_calculate_simple_match(student_id, student_skills, wl_positions):
        matches = []
        if student_skills is not None:
            s_categories = []
            s_sub_categories = []
            s_skills = []
            for ss in student_skills:
                if not ss['category_id'] in s_categories:
                    s_categories.append(int(ss['category_id']))
                if not ss['sub_category_id'] in s_sub_categories:
                    s_sub_categories.append(int(ss['sub_category_id']))
                for s in ss['skills']:
                    if not s['skill_Id'] in s_skills:
                        s_skills.append(int(s['skill_Id']))

            for position in wl_positions:
                if position['position_skill_list'] is not None:
                    r_categories = []
                    r_sub_categories = []
                    r_skills = []
                    for rs in position['position_skill_list']:
                        if not rs['category_id'] in r_categories:
                            r_categories.append(int(rs['category_id']))
                        if not rs['sub_category_id'] in r_sub_categories:
                            r_sub_categories.append((rs['sub_category_id']))
                        for s in rs['skills']:
                            if not s['skill_Id'] in r_skills:
                                r_skills.append(int(s['skill_Id']))

                    if r_categories.__len__() > 0:
                        match = Match(student_id=student_id, position_id=position['_id'])
                        match.source_skills = student_skills
                        match.regard_object_skills = position['position_skill_list']
                        match.category_similarity = match.calculate_similarity(r_categories, s_categories)
                        match.sub_categories_similarity = match.calculate_similarity(r_sub_categories, s_sub_categories)
                        match.skill_similarity = match.calculate_similarity(r_skills, s_skills)
                        match.match_level_id = match.calculate_match_level()
                        if match.match_level_id < 1:
                            matches.append(match)
        matches.sort(key=lambda ml: ml.match_level_id, reverse=True)
        return matches

    @staticmethod
    def wl_suggestion_skill_id(student_id, student_skills, wl_positions):
        matches = Match.wl_calculate_simple_match(student_id, student_skills, wl_positions)

        if not matches.__len__() > 0:
            return Match.wl_suggestion_skill_id(wl_positions=wl_positions)
        if matches[0].match_level_id == 0:
            return Match.wl_suggestion_skill_id(wl_positions=wl_positions)

        topMatched = matches[0]
        working_position = [x for x in wl_positions if x['_id'] == topMatched.position_id]
        ##check diff with categories

        s_categories = []
        s_sub_categories = []
        s_skills = []
        for ss in topMatched.source_skills:
            if not ss['category_id'] in s_categories:
                s_categories.append(int(ss['category_id']))
            if not ss['sub_category_id'] in s_sub_categories:
                s_sub_categories.append(int(ss['sub_category_id']))
            for s in ss['skills']:
                if not s['skill_Id'] in s_skills:
                    s_skills.append(int(s['skill_Id']))

        r_categories = []
        r_sub_categories = []
        r_skills = []
        for rs in topMatched.regard_object_skills:
            if not rs['category_id'] in r_categories:
                r_categories.append(int(rs['category_id']))
            if not rs['sub_category_id'] in r_sub_categories:
                r_sub_categories.append(int(rs['sub_category_id']))
            for s in rs['skills']:
                if not s['skill_Id'] in r_skills:
                    r_skills.append(int(s['skill_Id']))

        diff_categories = Match.diff_in_two_list(r_categories, s_categories)
        if diff_categories.__len__() > 0:
            new_skill = Match.get_skill_from_position_by_category(diff_categories[0],
                                                                  wl_position_skills=topMatched.regard_object_skills)
            new_student_skill = student_skills
            new_skill_obj = {
                'category_id': new_skill[0],
                'sub_category_id': new_skill[1],
                'skills': [
                    {
                        'skill_Id': new_skill[2]
                    }
                ]
            }
            new_student_skill.append(new_skill_obj)
            # recalc match level
            new_match_level = Match.wl_calculate_simple_match(student_id=student_id, student_skills=new_student_skill,
                                                              wl_positions=working_position)
            diff = (new_match_level[0].match_level_id - topMatched.match_level_id)

            result = {
                'new_skill': new_skill,
                'new_match_level_id': new_match_level[0].match_level_id,
                'old_match_level_id': topMatched.match_level_id,
                'diff': diff
            }

            return result
        elif diff_categories.__len__() == 0:  ## check diff with sub_categories
            diff_sub_categories = Match.diff_in_two_list(r_sub_categories, s_sub_categories)
            if diff_sub_categories.__len__() > 0:
                new_skill = Match.get_skill_from_position_by_sub_category(diff_sub_categories[0],
                                                                          wl_position_skills=topMatched.regard_object_skills)
                new_student_skill = student_skills

                new_skill_obj = {
                    'category_id': new_skill[0],
                    'sub_category_id': new_skill[1],
                    'skills': [
                        {
                            'skill_Id': new_skill[2]
                        }
                    ]
                }
                new_student_skill.append(new_skill_obj)

                new_match_level = Match.wl_calculate_simple_match(student_id=student_id,
                                                                  student_skills=new_student_skill,
                                                                  wl_positions=working_position)
                diff = (new_match_level[0].match_level_id - topMatched.match_level_id)

                result = {
                    'new_skill': new_skill,
                    'new_match_level_id': new_match_level[0].match_level_id,
                    'old_match_level_id': topMatched.match_level_id,
                    'diff': diff
                }

                return result
            else:
                diff_skills = Match.diff_in_two_list(r_skills, s_skills)
                if diff_skills.__len__() > 0:
                    new_skill = Match.get_skill_bt_skill_id(diff_skills[0],
                                                            wl_position_skills=topMatched.regard_object_skills)
                    new_student_skill = student_skills

                    index = -1
                    for idx, ss in enumerate(student_skills):
                        if ss['category_id'] == new_skill[0]:
                            if ss['sub_category_id'] == new_skill[1]:
                                index = idx

                    new_student_skill[index]['skills'].append({'skill_Id': new_skill[2]})

                    new_match_level = Match.wl_calculate_simple_match(student_id=student_id,
                                                                      student_skills=new_student_skill,
                                                                      wl_positions=working_position)
                    diff = (new_match_level[0].match_level_id - topMatched.match_level_id)

                    result = {
                        'new_skill': new_skill,
                        'new_match_level_id': new_match_level[0].match_level_id,
                        'old_match_level_id': topMatched.match_level_id,
                        'diff': diff
                    }
                    return result
                else:
                    return ""

    ##check diff with skills

    @staticmethod
    def wl_random_position_skill(wl_positions, student_skills=None):
        if wl_positions:

            skills = []
            for p in wl_positions:
                for rs in p.position_skill_list:
                    for s in rs['skills']:
                        skills.append(s['skill_Id'])

            index = random.randint(0, skills.__len__())

            if not student_skills:
                return skills[index]

        if student_skills:
            for stident_skill in student_skills:
                for ss in stident_skill['skills']:
                    skills.remove(ss['skill_Id'])
            return skills
        return None

    @staticmethod
    def diff_in_two_list(list1, list2):
        return list(set(list1) - set(list2))

    @staticmethod
    def get_skill_from_position_by_category(category_id, wl_position_skills):
        for s in wl_position_skills:
            if int(s['category_id']) == int(category_id):
                sub_category_id = int(s['sub_category_id'])
                skill_id = int(s['skills'][0]['skill_Id'])

        new_skill = [category_id, sub_category_id, skill_id]
        return new_skill

    @staticmethod
    def get_skill_from_position_by_sub_category(sub_category_id, wl_position_skills):
        for s in wl_position_skills:
            if int(sub_category_id) == int(s['sub_category_id']):
                category_id = int(s['category_id'])
                skill_id = int(s['skills'][0]['skill_Id'])

        new_skill = [category_id, sub_category_id, skill_id]
        return new_skill

    @staticmethod
    def get_skill_bt_skill_id(skill_id, wl_position_skills):
        for s in wl_position_skills:
            for ss in s['skills']:
                if int(ss['skill_Id']) == int(skill_id):
                    category_id = int(s['category_id'])
                    sub_category_id = int(s['sub_category_id'])

        new_skill = [category_id, sub_category_id, skill_id]
        return new_skill
