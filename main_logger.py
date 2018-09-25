import logging
from shutil import rmtree
from os import makedirs
from os.path import join


class MainLogger:

    def __init__(self, log_directory):

        # remove dirs
        rmtree(log_directory, ignore_errors=True)
        makedirs(log_directory)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # create logger
        logger = logging.getLogger("modDig")

        logger.setLevel(logging.DEBUG)

        # TBD
        # # create console handler and set level to debug
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        #
        # # add formatter to ch
        # ch.setFormatter(formatter)
        #
        # # add ch to logger
        # logger.addHandler(ch)

        # file handler
        self.log_file_path = join(log_directory, "modDig.log")
        fh = logging.FileHandler(self.log_file_path, mode='w')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        # add file handler to logger
        logger.addHandler(fh)
        self.logger = logger

    def get_log_lines(self):
        with open(self.log_file_path, "r") as log_file:
            lines = log_file.readlines()
            log_file.close()
            return lines

    def info(self, msg):
        self.logger.info(msg)
        logging.info(msg)

    def error(self, msg):
        self.logger.error(msg)
        logging.error(msg)

    def debug(self, msg):
        self.logger.debug(msg)
        logging.debug(msg)

    def console_error(self, msg):
        logging.error(msg)