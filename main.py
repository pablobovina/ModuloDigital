from source.experiment_reporter import ExperimentReporter
from source.experiment_scanner import ExperimentScanner
from time import sleep
from shutil import rmtree
from os import makedirs, getpid
import logging
import threading
from os.path import join


class ModDig(threading.Thread):

    def __init__(self, parent=None):
        self.parent = parent
        self.d = parent.data
        self.out_directory = parent.out_d
        self.error_directory = parent.error_d
        self.log_directory = parent.log_d

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
        rmtree(self.log_directory, ignore_errors=True)
        makedirs(self.log_directory)
        self.log_file_path = join(self.log_directory, "modDig.log")
        fh = logging.FileHandler(self.log_file_path, mode='w')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        # add file handler to logger
        logger.addHandler(fh)

        self.logger = logger
        self.name = "ModDig-{}-{}".format(parent.user, parent.id_thread)
        self.terminate_now = False

    def run(self):
        try:
            rmtree(self.out_directory, ignore_errors=True)
            makedirs(self.out_directory)
            experiment_scn = ExperimentScanner(self.d)
            experiment_rep = ExperimentReporter(experiment_scn, self.out_directory)
            for exp in experiment_rep:
                sleep(30)
                if self.terminate_now:
                    raise Exception("killed by manager")
                self.parent.on_partial(exp)
                self.parent.on_log(self.get_log_lines())
                pass

            end_file = join(self.out_directory, "end.txt")
            with open(end_file, "wb") as out:
                out.write("END RUN")
                self.logger.info("END RUN")
            self.parent.on_finish(self.get_log_lines())
        except Exception as e:
            if not self.terminate_now:
                self.parent.on_error(e.message, self.get_log_lines())
            elif self.terminate_now:
                self.parent.on_stop(e.message, self.get_log_lines())
            rmtree(self.error_directory, ignore_errors=True)
            makedirs(self.error_directory)
            error_file = join(self.error_directory, "error.log")
            with open(error_file, "wb") as out:
                out.write(e.message.__str__())

    def get_log_lines(self):
        with open(self.log_file_path, "r") as log_file:
            lines = log_file.readlines()
            log_file.close()
            return lines


if __name__ == "__main__":
    pass
