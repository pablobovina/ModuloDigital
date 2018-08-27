from experiment_data import *
from experiment_config import *
from experiment_scanner import *
import logging

logger = logging.getLogger("modDig")

class Experiment(ExperimentData, ExperimentConfig):

    def __init__(self, definition):

        assert isinstance(definition, ExperimentScanner)

        ExperimentData.__init__(self, definition.cpoints, definition.settings["a_times"])

        ExperimentConfig.__init__(self, definition.freq_set, definition.phase_set,
                                  definition.settings["a_bloq"], definition.settings["a_ts"])

    def __iter__(self):
        return ExperimentData.__iter__(self)

    def next(self):
        next_experiment = ExperimentData.next(self)
        logger.info("Reading experiment specs")
        return next_experiment

