from source.experiment_reporter import ExperimentReporter
from source.experiment_scanner import ExperimentScanner
from time import sleep
from os.path import join
from main_logger import MainLogger


class DryRun:

    def __init__(self, parent=None):
        self.parent = parent
        self.d = parent.data
        self.out_directory = parent.out_d
        self.error_directory = parent.error_d
        self.log_directory = parent.log_d
        self.logger = MainLogger(self.log_directory)
        self.terminate_now = False
        self.max_time = 1

    def run(self):
        try:
            experiment_scn = ExperimentScanner(self.d)
            experiment_rep = ExperimentReporter(experiment_scn, self.out_directory)
            counter = 0
            # runs one time
            for exp in experiment_rep:
                sleep(0)
                counter += 1
                if counter == self.max_time:
                    break
            end_file = join(self.out_directory, "end.txt")
            with open(end_file, "wb") as out:
                out.write("END RUN")
                self.logger.info("END RUN")
                out.close()
        except Exception as e:
            error_file = join(self.error_directory, "error.log")
            with open(error_file, "wb") as out:
                out.write(e.message.__str__())
                out.close()
                # log errors in console
                for m in e.message.split(";"):
                    self.logger.console_error(m)
            raise Exception(e.message)


if __name__ == "__main__":
    pass
