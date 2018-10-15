from math import floor
import logging
import re

logger = logging.getLogger("modDig")


class ExperimentScanner:

    LSB_LEN = 8
    MSB_LEN = 8
    MIN_TIME = 1
    MAX_TIME = 2 ** (32-1)
    N_FREQ = 2
    MAX_FREQ = 200000000
    MIN_FREQ = 0
    MIN_PHASE = 0
    MAX_PHASE = 360
    N_PHASE = 16
    MIN_DATA = 0
    MAX_DATA = 1024
    MIN_TS = 100
    MAX_TS = 254000
    phases_error = False
    freq_error = False

    def __init__(self, d):
        ExperimentScanner.phases_error = False
        ExperimentScanner.freq_errors = False
        errors = []
        parsed_data = ExperimentScanner._prepare_data(d, errors)
        self.freq_set = ExperimentScanner._scan_freq(parsed_data, errors)
        self.phase_set = ExperimentScanner._scan_phases(parsed_data, errors)
        self.cpoints = parsed_data["cpoints"]
        self.settings = parsed_data["settings"]

        if errors:
            for error in errors:
                logger.error(error)
            raise Exception("Scanner encontro algunas inconsitencias;" + ";".join(errors))

    @staticmethod
    def _prepare_data(d, errors):
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
        counter = 0
        for e in d["cpoints"]:
            # check cpoints
            try:
                e["time"] = [ExperimentScanner._time_to_ns(float(s.strip()), e["t_unit"], 40, errors, counter)
                             for s in e["time"].split(",")]
            except Exception as ex:
                errors.append("cpoint {} con demora {} error {}".format(counter, e["time"], ex.message))

            try:
                e["phase"] = [int(s.strip()) for s in e["phase"].split(",")]
            except Exception as ex:
                ExperimentScanner.phases_error = True
                errors.append("cpoint {} con phases {} error {}".format(counter, e["phase"], ex.message))

            try:
                e["freq"] = ExperimentScanner._freq_to_hz(float(e["freq"]), e["freq_unit"])
            except Exception as ex:
                ExperimentScanner.phases_error = True
                errors.append("cpoint {} on frecuencia {} error {}".format(counter, e["freq"], ex.message))

            try:
                e["data"] = int(e["data"])
                ExperimentScanner._check_data(e["data"], errors, counter)
            except Exception as ex:
                errors.append("cpoint {} con data {} error {}". format(counter, e["data"], ex. message))

            try:
                ExperimentScanner._check_lsb(e["lsb"], errors, counter)
            except Exception as ex:
                errors.append("cpoint {} con lsb error {}".format(counter, e["lsb"], ex.message))

            try:
                ExperimentScanner._check_msb(e["msb"], errors, counter)
            except Exception as ex:
                errors.append("cpoint {} con msb {} error {}".format(counter, e["msb"], ex.message))

            counter += 1
        # check settings
        try:
            d["settings"]["a_times"] = int(d["settings"]["a_times"])
        except Exception as ex:
            errors.append("settings con Times {} error {}".format(d["settings"]["a_times"], ex.message))

        try:
            d["settings"]["a_freq"] = ExperimentScanner._freq_to_hz(float(d["settings"]["a_freq"]), d["settings"]["a_freq_unit"])
        except Exception as ex:
            errors.append("settings con Frecuencia {} error {}".format(d["settings"]["a_freq"], ex.message))

        try:
            d["settings"]["a_ts"] = ExperimentScanner._time_to_ns(float(d["settings"]["a_ts"]), d["settings"]["a_ts_unit"], 1, errors)
        except Exception as ex:
            errors.append("settings con TS {} error {}".format(d["settings"]["a_ts"], ex.message))

        try:
            d["settings"]["a_bloq"] = int(d["settings"]["a_bloq"])
        except Exception as ex:
            errors.append("settings con Bloq {} error {}".format(d["settings"]["a_bloq"], ex.message))

        try:
            d["settings"]["a_channel"] = int(d["settings"]["a_channel"])
        except Exception as ex:
            errors.append("settings Channel {} error {}".format(d["settings"]["a_channel"], ex.message))

        try:
            d["settings"]["a_phase"] = [int(s.strip()) for s in d["settings"]["a_phase"].split(",")]
        except Exception as ex:
            errors.append("settings fases {} error {}".format(d["settings"]["a_phase"], ex.message))

        try:
            ExperimentScanner._check_lsb(d["settings"]["a_lsb"], errors)
        except Exception as ex:
            errors.append("settings lsb {} error {}".format(d["settings"]["a_lsb"], ex.message))

        try:
            ExperimentScanner._check_msb(d["settings"]["a_msb"], errors)
        except Exception as ex:
            errors.append("settings msb {} error {}".format(d["settings"]["a_msb"], ex.message))

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
    def _time_to_ns(t_val, t_unit, factor, errors, counter=None):
        res = None
        if t_unit == "ns":
            res = t_val
        if t_unit == "us":
            res = t_val * (10 ** 3)
        if t_unit == "ms":
            res = t_val * (10 ** 6)
        res = int(res / float(factor))

        # cpoints es para demora
        if counter is not None:
            if not ExperimentScanner.MIN_TIME <= res < ExperimentScanner.MAX_TIME:
                    msg_t = "cpoint {} con demora {} ns fuera de rango {} <= t <= {}"
                    msg = msg_t.format(counter, res, ExperimentScanner.MIN_TIME, ExperimentScanner.MAX_TIME)

        # settings es para el intervalo entre muestras del AD
        if counter is None and not ExperimentScanner.MIN_TS <= res <= ExperimentScanner.MAX_TS:
            msg_t = "settings con intervalo entre muestras {} ns fuera de rango {} <= t <= {}"
            msg = msg_t.format(res, ExperimentScanner.MIN_TS, ExperimentScanner.MAX_TS)
            errors.append(msg)

        return res

    @staticmethod
    def _scan_freq(d, errors):
        if ExperimentScanner.freq_error:
            errors.append("se omite barrido de frecuencias")
            return
        freq_set = set()
        # scan freq in cpoints
        counter = 0
        for e in d["cpoints"]:
            freq_set.add(e["freq"])
            if not ExperimentScanner.MIN_FREQ <= e["freq"] <= ExperimentScanner.MAX_FREQ:
                msg_t = "cpoint {} con freq {} Hz fuera de rango {} <= f <= {}"
                msg = msg_t.format(counter, e["freq"], ExperimentScanner.MIN_FREQ, ExperimentScanner.MAX_FREQ)
                errors.append(msg)
            counter += 1
        # scan freq in settings
        freq_set.add(d["settings"]["a_freq"])
        if not ExperimentScanner.MIN_FREQ <= d["settings"]["a_freq"] <= ExperimentScanner.MAX_FREQ:
            msg_t = "settings con freq {} Hz fuera de rango {} <= f <= {}"
            msg = msg_t.format(counter, d["settings"]["a_freq"], ExperimentScanner.MIN_FREQ, ExperimentScanner.MAX_FREQ)
            errors.append(msg)
        return freq_set

    @staticmethod
    def _scan_phases(d, errors):
        if ExperimentScanner.phases_error:
            errors.append("se omite barrido de fases")
            return
        phase_set = set()
        # scan phases in cpoints
        counter = 0
        for e in d["cpoints"]:
            for p in e["phase"]:
                phase_set.add(p)
                if not ExperimentScanner.MIN_PHASE <= p <= ExperimentScanner.MAX_PHASE:
                    msg_t = "cpoint {} con phase {} fuera de rango {} <= p <= {}"
                    msg = msg_t.format(counter, p, ExperimentScanner.MIN_PHASE, ExperimentScanner.MAX_PHASE)
                    errors.append(msg)
            counter += 1
        # scan phase in settings
        for p in d["settings"]["a_phase"]:
            phase_set.add(p)
            if not ExperimentScanner.MIN_PHASE <= p <= ExperimentScanner.MAX_PHASE:
                msg_t = "settings con phase {} fuera de rango {} <= p <= {}"
                msg = msg_t.format(p, ExperimentScanner.MIN_PHASE, ExperimentScanner.MAX_PHASE)
                errors.append(msg)
        return phase_set

    @staticmethod
    def _check_lsb(lsb, errors, counter=None):
        if len(lsb) != ExperimentScanner.LSB_LEN:
            if counter is not None:
                msg_t = "cpoint {} con lsb {} de longitud distinta a {}"
                msg = msg_t.format(counter, lsb, ExperimentScanner.LSB_LEN)
            else:
                msg_t = "settings con lsb {} de longitud distinta a {}"
                msg = msg_t.format(lsb, ExperimentScanner.LSB_LEN)
            errors.append(msg)

        if not re.match('[01]*$', lsb):
            if counter is not None:
                msg_t = "cpoint {} con lsb {} no binario"
                msg = msg_t.format(counter, lsb)
            else:
                msg_t = "settings con lsb {} no binario"
                msg = msg_t.format(lsb)
            errors.append(msg)

    @staticmethod
    def _check_msb(msb, errors, counter=None):
        if len(msb) != ExperimentScanner.LSB_LEN:
            if counter is not None:
                msg_t = "cpoint {} con msb {} de longitud distinta a {}"
                msg = msg_t.format(counter, msb, ExperimentScanner.LSB_LEN)
            else:
                msg_t = "settings con msb {} de longitud distinta a {}"
                msg = msg_t.format(msb, ExperimentScanner.LSB_LEN)
            errors.append(msg)

        if not re.match('[01]*$', msb):
            if counter is not None:
                msg_t = "cpoint {} con msb {} no binario"
                msg = msg_t.format(counter, msb)
            else:
                msg_t = "settings con lsb {} no binario"
                msg = msg_t.format(msb)
            errors.append(msg)

    @staticmethod
    def _check_data(data, errors, counter):
        if not ExperimentScanner.MIN_DATA <= data <= ExperimentScanner.MAX_DATA:
            msg_t = "cpoint {} con data {} fuera de rango {} <= d <= {}"
            msg = msg_t.format(counter, data, ExperimentScanner.MIN_DATA, ExperimentScanner.MAX_DATA)
            errors.append(msg)
