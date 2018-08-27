from experiment_runner import ExperimentRunner
import csv
import logging
import shutil
import os

logger = logging.getLogger("__main__")


class ExperimentReporter (ExperimentRunner):

    counter = 0

    def __init__(self, definition):
        ExperimentRunner.__init__(self, definition)
        shutil.rmtree("./out", ignore_errors=True)
        os.mkdir("./out")
        os.mkdir("./out/a")
        os.mkdir("./out/b")

    def __iter__(self):
        return ExperimentRunner.__iter__(self)

    def next(self):
        data_a, data_b = ExperimentRunner.next(self)
        self._make_csv_report(data_a, data_b)
        logger.info("CSV reports generated")
        self.counter += 1
        return data_a, data_b

    def _make_csv_report(self, data_a, data_b):
        with open("./out/a/{}_ca.csv".format(self.counter), "wb") as out:
            csv_out = csv.writer(out)
            csv_out.writerow(["x", "y"])
            for row in data_a:
                csv_out.writerow(row)

        with open("./out/b/{}_cb.csv".format(self.counter), "wb") as out:
            csv_out = csv.writer(out)
            csv_out.writerow(["x", "y"])
            for row in data_b:
                csv_out.writerow(row)
        return
