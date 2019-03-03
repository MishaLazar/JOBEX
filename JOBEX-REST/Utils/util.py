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
