from secuence import *
from ad import *
from pp2 import *
from dds2 import *
import csv
from tests import d1, d2, d3, d4, d5, d6
from math import floor


class Experiment:

    def __init__(self, d):
        definition = self._prepare_data(d)
        self.experiment = definition
        self.repeat = definition["settings"]["a_times"]
        self.experiment_iterable = definition
        self.secuence = None
        self.demora = 0

        self.pp2 = Pp2(delay=0)

        self.freq_set = set()
        self.phase_set = set()
        self._scan_freq_phases()
        self.dds2 = Dds2(self.freq_set, self.phase_set, delay=0)

        self.ad = Ad(bloqnum=definition["settings"]["a_bloq"], inter_ts=definition["settings"]["a_ts"])
        self.ad_channel = definition["settings"]["a_channel"]
        self.ad.configure()

        print "_" * 80

    def __iter__(self):
        return self

    def next(self):
        if self.repeat == 1:
            self.repeat -= 1
            return self.experiment_iterable
        if self.repeat > 1:
            for e in self.experiment_iterable["cpoints"]:
                l = e["phase"]
                e["phase"] = l[1:] + l[:1]
            self.repeat -= 1
            return self.experiment_iterable
        if self.repeat <= 0:
            raise StopIteration()

    def _get_dir_phase(self, phase):
        return self.dds2.get_dir_phase(phase)

    def _get_dir_freq(self, freq):
        return self.dds2.get_dir_freq(freq)

    def _get_pattern(self, pulsos, freq, phase, load_ram="0", udclk="0", disparo_ad="0", pulso_test=None):
        p = self._get_dir_phase(phase)
        p_1 = "0" * (4 - len("{0:b}".format(p))) + "{0:b}".format(p)
        f = self._get_dir_freq(freq)
        f_1 = "0" * (1 - len("{0:b}".format(f))) + "{0:b}".format(f)
        # (16 15)-(14 13 12 11)-(10)-(9)-(8)-(7 6)-(5)-(4  3  2  1)
        # a  b    c  d  e  f    g    h   i   j k   l   m  n  o  p
        # 0  1    2  3  4  5    6    7   8   9 10  11  12 13 14 15
        s = pulsos[0:2] + p_1 + udclk + load_ram + f_1 + pulsos[9:11] + disparo_ad + pulsos[12:16]
        if pulso_test:
            s = pulso_test + pulsos[1:2] + p_1 + udclk + load_ram + f_1 + pulsos[9:11] + disparo_ad + pulsos[12:16]

        return s

    def _reset_secuence(self):
        self.secuence = Secuence()

    def _reset_demora(self):
        self.demora = 0

    def _translate2(self, counter=0, ins=0, loops=[]):
        cpoints = self.experiment_iterable["cpoints"]
        if counter >= len(cpoints):
            pulso_5 = "0000000000010000"
            self.secuence.cont(pulso_5, 0)
            self.secuence.end()
            return True

        if len(loops) > 4:
            return False

        lsb = cpoints[counter]["lsb"]
        msb = cpoints[counter]["msb"]
        demora = cpoints[counter]["time"]
        freq = cpoints[counter]["freq"]
        phase = cpoints[counter]["phase"][0]

        if cpoints[counter]["type"] == "C":
            # carga fase en ram
            p_load_ram = self._get_pattern(pulsos=lsb + msb, freq=freq, phase=phase, load_ram="1")
            demora_load_ram = 2
            self.secuence.cont(p_load_ram, demora_load_ram)
            ins += 1
            # carga fase en registro trabajo con pulso udlck
            p_udclk = self._get_pattern(pulsos=lsb + msb, freq=freq, phase=phase, load_ram="0", udclk="1")
            demora_udclk = 2
            self.secuence.cont(p_udclk, demora_udclk)
            ins += 1
            # carga de la instruccion original
            p = self._get_pattern(pulsos=lsb + msb, freq=freq, phase=phase)
            self.secuence.cont(p, demora)
            ins += 1
            # si pertenece a un loop acumulamos la demora ahi
            # sino va  la demora gral

            if loops:
                l = loops.pop()
                l["demora"] += demora + demora_load_ram + demora_udclk
                loops.append(l)
            else:
                self.demora += demora
            counter += 1
            return self._translate2(counter, ins, loops)

        if cpoints[counter]["type"] == "R":
            l = loops.pop()
            if not l:
                # un return in loop
                return False

            p = self._get_pattern(pulsos=lsb + msb, freq=freq, phase=phase)
            data = l["data"]
            lazo = l["lazo"]
            t = l["demora"]
            rep = l["rep"]

            self.secuence.retl(p, data, lazo, demora)
            ins += 1
            # ctualizamos demora acumulada
            if loops:
                l = loops.pop()
                l["demora"] += (demora+t)*rep
                loops.append(l)
            else:
                self.demora += (demora+t)*rep
            counter += 1
            return self._translate2(counter, ins, loops)

        if cpoints[counter]["type"] == "L":
            n = cpoints[counter]["data"]
            lazo = len(loops)
            loops.append({"data": ins, "lazo": lazo, "demora": demora, "rep": n})
            p = self._get_pattern(pulsos=lsb + msb, freq=freq, phase=phase)
            self.secuence.lazo(p, n, lazo, demora)
            ins += 1
            counter += 1
            return self._translate2(counter, ins, loops)

    def run(self):
        self._reset_secuence()
        self._reset_demora()
        self._translate2(0, 0, [])
        self.pp2.upload_program(self.secuence)
        self.pp2.trigger_program()
        self._wait_end_run()
        self.ad.read_channels()

        data_a = self.ad.data_a
        data_b = self.ad.data_b

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

    def _wait_end_run(self):
        # base 40 nanosec
        t = (self.demora * 40) * (10 ** -9)
        print t
        sleep(t)

    def _prepare_data(self, d):
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
        }

        """
        for e in d["cpoints"]:
            e["time"] = self._time_to_ns(float(e["time"]), e["t_unit"], 40)
            e["phase"] = [int(s.strip()) for s in e["phase"].split(",")]
            e["freq"] = self._freq_to_hz(float(e["freq"]), e["freq_unit"])
            e["data"] = int(e["data"])

        d["settings"]["a_times"] = int(d["settings"]["a_times"])
        d["settings"]["a_freq"] = int(d["settings"]["a_freq"])
        d["settings"]["a_ts"] = self._time_to_ns(float(d["settings"]["a_ts"]), d["settings"]["a_ts_unit"], 1)
        d["settings"]["a_bloq"] = int(d["settings"]["a_bloq"])
        d["settings"]["a_channel"] = int(d["settings"]["a_channel"])

        return d

    def _scan_freq_phases(self):
        for e in self.experiment["cpoints"]:
            self.freq_set.add(e["freq"])
            for p in e["phase"]:
                self.phase_set.add(p)

    def _freq_to_hz(self, f_val, f_unit):
        res = None
        if f_unit == "hz":
            res = f_val
        if f_unit == "mhz":
            res = f_val * (10 ** 6)
        return int(floor(res))

    def _time_to_ns(self, t_val, t_unit, factor):
        res = None
        if t_unit == "ns":
            res = t_val
        if t_unit == "us":
            res = t_val * (10 ** 3)
        if t_unit == "ms":
            res = t_val * (10 ** 6)
        return int(res / float(factor))


if __name__ == "__main__":
    ex = Experiment(d6)
    ex.run()
    for e in ex:
        ex.run()
        print "_" * 80
