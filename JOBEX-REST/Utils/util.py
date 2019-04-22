from collections import defaultdict

class Utils:

    @staticmethod
    def parse_url_data(data):
        data_list = data.split('&')
        rest_name = data_list[0]
        user_data = data_list[1].split('=')
        user_id = user_data[1]
        return (rest_name, user_id)

    @staticmethod
    def clean_string(string_data):
        string_data = string_data.replace('\r', '')
        string_data = string_data.replace('\n', '')
        return string_data

    #if __name__ == "__main__":
    #    result_list = [{"HELP:ops"}]
    #    print(result_list[0])

    @staticmethod
    def int_try_parse(value, default_value):
        try:
            return int(value)
        except ValueError:
            return default_value

    @staticmethod
    def skill_string_array_to_object(position_skills_metadata_list):
        """ position_skills_metadata_list for example: 1,2,3
         where 1 is skill_id, 2 is skill_sub_cat and 3 is skill_cat """
        position_skill_list = defaultdict(list)
        for position_skills_metadata in position_skills_metadata_list:
            skill_id = position_skills_metadata.split(",")[0]
            sub_cat_id = position_skills_metadata.split(",")[1]
            cat_id = position_skills_metadata.split(",")[2]
            key = (cat_id, sub_cat_id)
            position_skill_list[key].append({"skill_Id": skill_id})
        items = []
        for item in position_skill_list.items():
            items.append({"category_id": item[0][0], "sub_category_id": item[0][1], "skills": item[1]})
        return items
