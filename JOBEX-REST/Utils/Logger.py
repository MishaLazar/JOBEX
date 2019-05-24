import logging
from Utils.config_helper import ConfigHelper

config = ConfigHelper.get_instance()


class Logger:

    def __init__(self, name):
        logging_level = config.read_logger(Key="LOGGER_LEVEL")

        self.logger = logging.getLogger(name)

        fh = logging.FileHandler(config.read_logger('LOG_PATH'), mode='w', encoding=None, delay=False)
        if logging_level == 'ERROR':
            self.logger.setLevel(logging.ERROR)
            fh.setLevel(logging.ERROR)
        elif logging_level == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
            fh.setLevel(logging.DEBUG)
        elif logging_level == 'INFO':
            self.logger.setLevel(logging.INFO)
            fh.setLevel(logging.INFO)
        elif logging_level == 'WARNING':
            self.logger.setLevel(logging.WARNING)
            fh.setLevel(logging.WARNING)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
