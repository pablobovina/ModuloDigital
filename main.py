from source.experiment_reporter import ExperimentReporter
from source.experiment_scanner import ExperimentScanner
from time import sleep
import threading
from os.path import join
from main_logger import MainLogger
from source.setup import SetupModDig


class ModDig(threading.Thread):

    def __init__(self, parent=None):
        threading.Thread.__init__(self)
        self.parent = parent
        self.d = parent.data
        self.out_directory = parent.out_d
        self.error_directory = parent.error_d
        self.log_directory = parent.log_d
        self.logger = MainLogger(self.log_directory)
        self.name = "ModDig-{}-{}".format(parent.user, parent.id_thread)
        self.terminate_now = False
        SetupModDig(debug=False)

    def run(self):
        experiment_rep = None
        try:
            experiment_scn = ExperimentScanner(self.d)
            experiment_rep = ExperimentReporter(experiment_scn, self.out_directory)
            for exp in experiment_rep:
                if self.terminate_now:
                    raise Exception("killed by manager")
                self.parent.on_partial(exp)
                self.parent.on_log(self.logger.get_log_lines())
                sleep(0)
                pass

            # shut down pp2 and dds2
            experiment_rep.dds2.deactivate()
            experiment_rep.pp2.reset()

            # mark end run
            end_file = join(self.out_directory, "end.txt")
            with open(end_file, "wb") as out:
                out.write("END RUN")
                self.logger.info("END RUN")
            self.parent.on_finish(self.logger.get_log_lines())

        except Exception as e:
            if not self.terminate_now:
                self.parent.on_error(e.message, self.logger.get_log_lines())
            elif self.terminate_now:
                self.parent.on_stop(e.message, self.logger.get_log_lines())
            error_file = join(self.error_directory, "error.log")
            with open(error_file, "wb") as out:
                out.write(e.message.__str__())
            # log errors in console
            for m in e.message.split(";"):
                self.logger.console_error(m)

            # shut down pp2 and dds2
            if experiment_rep:
                experiment_rep.dds2.deactivate()
                experiment_rep.pp2.reset()


if __name__ == "__main__":
    pass
