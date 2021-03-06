import configparser


class ConfigHelper:
    config = configparser.ConfigParser()

    def __init__(self, filePath=None):
        if filePath is None:
            # default config
            self.config.read('../jobex-web-app/Configurations.ini')
        else:
            self.config.read(filePath)

    def readRestParams(self, Key=None):
        if Key is None:
            return None
        else:
            return self.config['RESTPARAMS'][Key]

    def readAppSettings(self, Key=None):
        if Key is None:
            return None
        else:
            return self.config['APPSETTINGS'][Key]
