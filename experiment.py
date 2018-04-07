from secuence import *
from ad import *
from pp2 import *
from dds2 import *
import csv

# experimento de ejemplo
# analizar loop con respecto a freq y phase entrada-salida
exp = {"cpoints": 
    [
        {"type": "continue", "pattern": "1" * 16, "demora": 4000000, "freq": 100000, "phase": [0, 90, 180, 270]},
        {"type": "loop", "pattern_init": "0" * 16, "pattern_end": "0" * 16, "ntimes": 5,
            "freq_init": 150000, "phase_init": [0, 90, 180, 270],
            "freq_end": 150000, "phase_end": [0, 90, 180, 270], "demora": 0, "instructions":
            [
                {"type": "continue", "pattern": "0" * 16, "demora": 4000000, "freq": 100000, "phase": [0, 90, 180, 270]},
                {"type": "continue", "pattern": "1" * 16, "demora": 4000000, "freq": 150000, "phase": [0, 90, 180, 270]}
            ]
         },
        {"type": "continue", "pattern": "0" *16, "demora": 4000000, "freq": 100000, "phase": [0, 90, 180, 270]},
        {"type": "loop", "pattern_init": "0" * 16, "pattern_end": "0" * 16, "ntimes": 5,
            "freq_init": 150000, "phase_init": [0, 90, 180, 270],
            "freq_end": 150000, "phase_end": [0, 90, 180, 270], "demora": 0, "instructions":
            [
                {"type": "continue", "pattern": "0" * 16, "demora": 4000000, "freq": 100000, "phase": [0, 90, 180, 270]},
                {"type": "continue", "pattern": "1" * 16, "demora": 4000000, "freq": 150000, "phase": [0, 90, 180, 270]}
            ]
        }
    ],
    "repeat": 2,
    "ad": {"ts": 1000, "bloq": 1, "channels": 3},
    "name": "experimento de pruebas",
    "date": "11:00:00T05/03/2018",
    "author": "pbovina"
}


class Experiment:

    def __init__(self, definition):
        self.experiment = definition
        self.repeat = definition["repeat"]
        self.experiment_iterable = definition
        self.secuence = None
        self.demora = 0

        self.pp2 = Pp2(delay=0)

        self.freq_set = set()
        self.phase_set = set()

        for e in self.experiment["cpoints"]:
            if e["type"] == "continue":
                self.freq_set.add(e["freq"])
                self.phase_set = self.phase_set.union(set(e["phase"]))
                self.demora += e['demora']
            elif e["type"] == "loop":
                self.freq_set.add(e["freq_init"])
                self.phase_set = self.phase_set.union(set(e["phase_init"]))
                self.freq_set.add(e["freq_end"])
                self.phase_set = self.phase_set.union(set(e["phase_end"]))
                demora_loop = e['demora']
                for ins in e["instructions"]:
                    self.freq_set.add(ins["freq"])
                    self.phase_set = self.phase_set.union(set(ins["phase"]))
                    demora_loop += ins['demora']
                self.demora = self.demora + (demora_loop * e['ntimes'])

        self.dds2 = Dds2(self.freq_set, self.phase_set, delay=0)

        self.ad = Ad(delay=0, bloqnum=definition["ad"]["bloq"],
                     inter_ts=definition["ad"]["ts"],
                     channel=definition["ad"]["channels"])
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
                self._shift(e)
            self.repeat -= 1
            return self.experiment_iterable
        if self.repeat <= 0:
            raise StopIteration()

    def _shift(self, e):
        if e["type"] == "continue":
            l = e["phase"]
            e["phase"] = l[1:] + l[:1]
        elif e["type"] == "loop":
            for f in e["instructions"]:
                self._shift(f)
        return

    def _get_dir_phase(self, phase):
        return self.dds2.get_dir_phase(phase)

    def _get_dir_freq(self, freq):
        return self.dds2.get_dir_freq(freq)

    def _get_pattern(self, pulsos, freq, phase, disparo_sec="0", udclk="0", disparo_ad="0"):
        p = self._get_dir_phase(phase)
        p_1 = "0" * (4 - len("{0:b}".format(p))) + "{0:b}".format(p)
        f = self._get_dir_freq(freq)
        f_1 = "0" * (1 - len("{0:b}".format(f))) + "{0:b}".format(f)
        #(16 15)-(14 13 12 11)-(10)-(9)-(8)-(7 6)-(5)-(4  3  2  1)
        # a  b    c  d  e  f    g    h   i   j k   l   m  n  o  p
        # 0  1    2  3  4  5    6    7   8   9 10  11  12 13 14 15
        s = pulsos[0:2] + p_1 + disparo_sec + udclk + f_1 + pulsos[9:11] + disparo_ad + pulsos[12:16]
        return s

    def _translate(self):
        sec = Secuence()
        ins_counter = 0
        pulso_5 = "0000000000010000"
        for cmd in self.experiment_iterable["cpoints"]:
            if cmd["type"] == "continue":
                p = self._get_pattern(cmd["pattern"], cmd["freq"], cmd["phase"][0])
                t = cmd["demora"]
                sec.cont(p, t)
                ins_counter += 1
            elif cmd["type"] == "loop":
                p = self._get_pattern(cmd["pattern_init"], cmd["freq_init"], cmd["phase_init"][0])
                d = cmd["ntimes"]
                l = 0
                t = cmd["demora"]
                sec.lazo(p, d, l, t)
                loop_dir = ins_counter
                ins_counter += 1
                for cmd_loop in cmd["instructions"]:
                    p = self._get_pattern(cmd_loop["pattern"], cmd_loop["freq"], cmd_loop["phase"][0])
                    t = cmd_loop["demora"]
                    sec.cont(p, t)
                    ins_counter += 1
                p = self._get_pattern(cmd["pattern_end"], cmd["freq_end"], cmd["phase_end"][0])
                d = loop_dir
                l = 0
                t = cmd["demora"]
                sec.retl(p, d, l, t)
                ins_counter += 1
        sec.cont(pulso_5, 0)
        sec.end()
        self.secuence = sec
        return

    def run(self):
        self._translate()
        self.pp2.upload_program(self.secuence)
        self.pp2.trigger_program()
        self._wait_end_run()
        self.ad.read_channels()

        data_a = self.ad.data_a
        data_b = self.ad.data_b

        with open('canal_a.csv', 'wb') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(['x', 'y'])
            for row in data_a:
                csv_out.writerow(row)

        with open('canal_b.csv', 'wb') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(['x', 'y'])
            for row in data_b:
                csv_out.writerow(row)
        return

    def _wait_end_run(self):
        #base 40 nanosec
        t = (self.demora * 40) * (10**-9)
        print t
        sleep(t)

if __name__ == "__main__":
    ex = Experiment(exp)
    ex.run()
    for e in ex:
        ex.run()
        print "_" * 80
