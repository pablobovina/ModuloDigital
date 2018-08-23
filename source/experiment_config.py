from ad import Ad
from dds2 import Dds2
import logging

logger = logging.getLogger("__main__")

class ExperimentConfig:

    def __init__(self, freq_set, phase_set, bloq, inter_ts):
        self.dds2 = Dds2(freq=freq_set, phase=phase_set, delay=0)
        self.ad = Ad(bloqnum=bloq, inter_ts=inter_ts)
        self.freq_dirs = self.dds2.freq_table
        self.phase_dirs = self.dds2.phase_table
        logger.info("AD configurated")
        logger.info("DDS2 configurated")
