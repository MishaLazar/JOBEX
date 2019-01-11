import threading
import time
import logging
from config_helper import ConfigHelper

config = ConfigHelper.get_instance()
class JobThread(threading.Thread):
    def __init__(self):
        super(JobThread, self).__init__()
        self.iterations = 0
        self.daemon = True  # Allow main to exit even if still running.
        self.paused = True  # Start out paused.
        self.state = threading.Condition()

        self.logger = logging.getLogger(name='JOB_THREAD')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(config.read_logger('LOG_PATH'),mode='a', encoding=None, delay=False)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def run(self):
        self.resume()
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            # Do stuff.
            self.do_job()
            time.sleep(int(config.read_job('DELAY_INTERVAL')))
            self.iterations += 1

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

    def pause(self):
        with self.state:
            self.paused = True  # Block self.

    def do_job(self):
        self.logger.debug('do_job')
        # TODO:fetch jobs data and process



job = JobThread()
job.run()