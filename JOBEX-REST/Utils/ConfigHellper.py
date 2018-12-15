import configparser

class configHellper:

    config = configparser.ConfigParser()

    def __init__(self,filePath=None):
        if filePath is None:
            # default config
            self.config.read('../JOBEX-REST/Configurations.ini')
        else:
            self.config.read(filePath)

    def readDbParams(self,Key=None):
        if Key is None:
            return None
        else:
            return self.config['DBPARAMS'][Key]

    def readAppSettings(self,Key=None):
        if Key is None:
            return None
        else:
            return self.config['APPSETTINGS'][Key]
