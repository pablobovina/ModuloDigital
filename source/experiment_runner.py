from experiment_secuence import ExperimentSecuence
from pp2 import Pp2
import logging

logger = logging.getLogger("modDig")


class ExperimentRunner (ExperimentSecuence):

    def __init__(self, definition):
        ExperimentSecuence.__init__(self, definition)
        self.pp2 = Pp2()

    def __iter__(self):
        return ExperimentSecuence.__iter__(self)

    def next(self):
        secuence, duration = ExperimentSecuence.next(self)
        self.pp2.upload_program(secuence)
        logger.info("Uploaded Program PP2")
        self.pp2.trigger_program()
        logger.info("Triggered Program PP2")
        self.pp2.wait_end_run()
        logger.info("Finished run PP2")
        self.ad.read_channels()
        logger.info("Already data from AD")
        return self.ad.data_a, self.ad.data_b
