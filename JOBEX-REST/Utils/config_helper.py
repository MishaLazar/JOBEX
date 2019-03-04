import configparser


class ConfigHelper:

    config = configparser.ConfigParser()

    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if ConfigHelper.__instance == None:
            ConfigHelper()
        return ConfigHelper.__instance

    def __init__(self, file_path= None):
        if file_path is None:
            # default config
            self.config.read('../JOBEX-REST/Configurations.ini')
        else:
            self.config.read(file_path)

        if ConfigHelper.__instance != None:
            ConfigHelper.__instance
        else:
            ConfigHelper.__instance = self

    @staticmethod
    def read_db_params(Key=None):
        if Key is None:
            return None
        else:
            return ConfigHelper.__instance.config['DBPARAMS'][Key]

    @staticmethod
    def read_app_settings(Key=None):
        if Key is None:
            return None
        else:
            return ConfigHelper.__instance.config['APPSETTINGS'][Key]

    @staticmethod
    def read_auth(Key=None):
        if Key is None:
            return None
        else:
            return ConfigHelper.__instance.config['AUTH'][Key]

    @staticmethod
    def read_job(Key=None):
        if Key is None:
            return None
        else:
            return ConfigHelper.__instance.config['JOBPARAMS'][Key]

    @staticmethod
    def read_sentiment(Key=None):
        if Key is None:
            return None
        else:
            return ConfigHelper.__instance.config['SENTIMENT'][Key]

    @staticmethod
    def read_logger(Key=None):
        if Key is None:
            return 10
        else:
            return ConfigHelper.__instance.config['LOGGER'][Key]

