from experiment_runner import ExperimentRunner
import csv


class ExperimentReporter (ExperimentRunner):

    def __init__(self, definition):
        ExperimentRunner.__init__(self, definition)

    def __iter__(self):
        return ExperimentRunner.__iter__(self)

    def next(self):
        data_a, data_b = ExperimentRunner.next(self)
        ExperimentReporter._make_csv_report(data_a, data_b)
        return data_a, data_b

    @staticmethod
    def _make_csv_report(data_a, data_b):
        with open("canal_a.csv", "wb") as out:
            csv_out = csv.writer(out)
            csv_out.writerow(["x", "y"])
            for row in data_a:
                csv_out.writerow(row)

        with open("canal_b.csv", "wb") as out:
            csv_out = csv.writer(out)
            csv_out.writerow(["x", "y"])
            for row in data_b:
                csv_out.writerow(row)
        return
