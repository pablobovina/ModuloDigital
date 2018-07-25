from tests import d6
from experiment_reporter import ExperimentReporter
from experiment_scanner import ExperimentScanner


def main(d):
    experiment_scn = ExperimentScanner(d)
    experiment_rep = ExperimentReporter(experiment_scn)
    for exp in experiment_rep:
        print exp


if __name__ == "__main__":
    main(d6)
