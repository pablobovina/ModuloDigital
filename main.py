from tests import d6
from source.experiment_reporter import ExperimentReporter
from source.experiment_scanner import ExperimentScanner
from time import sleep
from shutil import rmtree
from os import makedirs
import logging
import threading
from os.path import join


class ModDig(threading.Thread):

    def __init__(self, d, out_dir, log_dir, error_dir):
        threading.Thread.__init__(self)
        # create logger
        logger = logging.getLogger("modDig")
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        # file handler
        rmtree(log_dir, ignore_errors=True)
        makedirs(log_dir)
        self.log_directory = log_dir
        log_file = join(self.log_directory, "modDig.log")
        fh = logging.FileHandler(log_file, mode='w')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        # add file handler to logger
        logger.addHandler(fh)
        self.d = d
        self.logger = logger
        self.out_directory = out_dir
        self.error_directory = error_dir

    def run(self):
        try:
            rmtree(self.out_directory, ignore_errors=True)
            makedirs(self.out_directory)
            experiment_scn = ExperimentScanner(self.d)
            experiment_rep = ExperimentReporter(experiment_scn, self.out_directory)
            for exp in experiment_rep:
                sleep(5)
                pass

            end_file = join(self.out_directory, "end.txt")
            with open(end_file, "wb") as out:
                out.write("END RUN")
                self.logger.info("END RUN")

        except Exception as e:
            rmtree(self.error_directory, ignore_errors=True)
            makedirs(self.error_directory)
            error_file = join(self.error_directory, "error.log")
            with open(error_file, "wb") as out:
                out.write(e.message.__str__())


if __name__ == "__main__":
    ModDig(d6, "./out", "./log", "./error").start()
