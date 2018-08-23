from tests import d6
from source.experiment_reporter import ExperimentReporter
from source.experiment_scanner import ExperimentScanner
from time import sleep

import logging

# create logger
logger = logging.getLogger(__name__)
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
fh = logging.FileHandler("main.log", mode='w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# add file handler to logger
logger.addHandler(fh)

def main(d):
    experiment_scn = ExperimentScanner(d)
    experiment_rep = ExperimentReporter(experiment_scn)
    for exp in experiment_rep:
        sleep(0)
        pass    

if __name__ == "__main__":
    main(d6)
