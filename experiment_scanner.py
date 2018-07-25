from math import floor


class ExperimentScanner:

    def __init__(self, d):
        parsed_data = ExperimentScanner._prepare_data(d)
        self.cpoints = parsed_data["cpoints"]
        self.freq_set = ExperimentScanner._scan_freq(parsed_data)
        self.phase_set = ExperimentScanner._scan_phases(parsed_data)
        self.settings = parsed_data["settings"]

    @staticmethod
    def _prepare_data(d):
        """
        {"lsb": "1" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "C", "msb": "1" * 8, "time": "4000000",
             "phase": "0, 90, 180, 270", "freq": "100000", "data": "0", "id": 1523141654228L}

        "settings": {
            "a_times": "0",
            "a_name": "Experimento de pruebas",
            "a_description": "Este es un experimento de pruebas",
            "a_freq": "100",
            "a_msb": "10000001",
            "a_freq_unit": "mhz",
            "a_ts_unit": "us",
            "a_lsb": "10000001",
            "a_ts": "1000",
            "a_bloq": "1",
            "a_channel": "3",
            "a_phase":"0"
        }

        """
        for e in d["cpoints"]:
            e["time"] = ExperimentScanner._time_to_ns(float(e["time"]), e["t_unit"], 40)
            e["phase"] = [int(s.strip()) for s in e["phase"].split(",")]
            e["freq"] = ExperimentScanner._freq_to_hz(float(e["freq"]), e["freq_unit"])
            e["data"] = int(e["data"])

        d["settings"]["a_times"] = int(d["settings"]["a_times"])
        d["settings"]["a_freq"] = ExperimentScanner._freq_to_hz(float(d["settings"]["a_freq"]), d["settings"]["a_freq_unit"])
        d["settings"]["a_ts"] = ExperimentScanner._time_to_ns(float(d["settings"]["a_ts"]), d["settings"]["a_ts_unit"], 1)
        d["settings"]["a_bloq"] = int(d["settings"]["a_bloq"])
        d["settings"]["a_channel"] = int(d["settings"]["a_channel"])

        return d

    @staticmethod
    def _freq_to_hz(f_val, f_unit):
        res = None
        if f_unit == "hz":
            res = f_val
        if f_unit == "mhz":
            res = f_val * (10 ** 6)
        return int(floor(res))

    @staticmethod
    def _time_to_ns(t_val, t_unit, factor):
        res = None
        if t_unit == "ns":
            res = t_val
        if t_unit == "us":
            res = t_val * (10 ** 3)
        if t_unit == "ms":
            res = t_val * (10 ** 6)
        return int(res / float(factor))

    @staticmethod
    def _scan_freq(d):
        freq_set = set()
        for e in d["cpoints"]:
            freq_set.add(e["freq"])
        return freq_set

    @staticmethod
    def _scan_phases(d):
        phase_set = set()
        for e in d["cpoints"]:
            for p in e["phase"]:
                phase_set.add(p)
        return phase_set
