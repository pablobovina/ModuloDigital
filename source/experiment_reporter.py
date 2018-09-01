from experiment_runner import ExperimentRunner
import csv
import logging
from os.path import join
from shutil import rmtree
from os import makedirs

logger = logging.getLogger("modDig")


class ExperimentReporter (ExperimentRunner):

    counter = 0

    def __init__(self, definition, directory):
        ExperimentRunner.__init__(self, definition)
        self.report_dir = directory
        rmtree(join(directory, "a"), ignore_errors=True)
        rmtree(join(directory, "b"), ignore_errors=True)
        makedirs(join(directory, "a"))
        makedirs(join(directory, "b"))

    def __iter__(self):
        return ExperimentRunner.__iter__(self)

    def next(self):
        data_a, data_b = ExperimentRunner.next(self)
        self._make_csv_report(data_a, data_b)
        logger.info("CSV reports generated")
        self.counter += 1
        return data_a, data_b

    def _make_csv_report(self, data_a, data_b):
        ca_file = join(self.report_dir, "a", "{}_ca.csv".format(self.counter))
        with open(ca_file, "wb") as out:
            csv_out = csv.writer(out)
            csv_out.writerow(["x", "y"])
            for row in data_a:
                csv_out.writerow(row)

        cb_file = join(self.report_dir, "b", "{}_cb.csv".format(self.counter))
        with open(cb_file, "wb") as out:
            csv_out = csv.writer(out)
            csv_out.writerow(["x", "y"])
            for row in data_b:
                csv_out.writerow(row)
        return
