from experiment2 import Experiment
from secuence import Secuence
import logging

logger = logging.getLogger("modDig")


class ExperimentSecuence(Experiment):

    def __init__(self, definition):
        Experiment.__init__(self, definition)

    def __iter__(self):
        return Experiment.__iter__(self)

    def next(self):
        cpoints = Experiment.next(self)
        logger.info("Generating pulse secuence")
        pulse_secuence = ExperimentSecuence._translate(cpoints, Secuence(), 0, 0, 0, [], self.freq_dirs, self.phase_dirs)
        return pulse_secuence

    @staticmethod
    def _translate(cpoints, secuence, demora, counter, ins, loops, freq_dirs, phase_dirs):

        if counter >= len(cpoints) and not loops:
            secuence.end()
            return secuence, demora

        if counter >= len(cpoints) and loops:
            raise Exception("secuencia mal formada: loops sin return")
            
        if len(loops) > 4:
            raise Exception("secuencia mal formada: el numero de loops anidados es mayor a 4")

        lsb = cpoints[counter]["lsb"]
        msb = cpoints[counter]["msb"]
        time_cp = cpoints[counter]["time"]
        freq = cpoints[counter]["freq"]
        phase = cpoints[counter]["phase"][0]

        if cpoints[counter]["type"] == "C":
            # carga fase en ram
            p_load_ram = ExperimentSecuence._get_pattern(pulsos="0"*16, freq=freq, phase=phase,
                                                         freq_dirs=freq_dirs, phase_dirs=phase_dirs,
                                                         load_ram="1", udclk="0", disparo_ad="0")
            demora_load_ram = 2
            secuence.cont(p_load_ram, demora_load_ram)
            ins += 1
            # carga fase en registro trabajo con pulso udlck
            p_udclk = ExperimentSecuence._get_pattern(pulsos="0"*16, freq=freq, phase=phase,
                                                      freq_dirs=freq_dirs, phase_dirs=phase_dirs,
                                                      load_ram="0", udclk="1", disparo_ad="0")
            demora_udclk = 2
            secuence.cont(p_udclk, demora_udclk)
            ins += 1
            # carga de la instruccion original
            p = ExperimentSecuence._get_pattern(pulsos=lsb + msb, freq=freq, phase=phase,
                                                freq_dirs=freq_dirs, phase_dirs=phase_dirs)
            secuence.cont(p, time_cp)
            ins += 1
            # si pertenece a un loop acumulamos la demora ahi
            # sino va  la demora gral

            if loops:
                top_loop = loops.pop()
                top_loop["demora"] += time_cp + demora_load_ram + demora_udclk
                loops.append(top_loop)
            else:
                demora += time_cp + demora_load_ram + demora_udclk
            counter += 1
            return ExperimentSecuence._translate(cpoints, secuence, demora, counter, ins, loops, freq_dirs, phase_dirs)

        if cpoints[counter]["type"] == "R":
            if len(loops):
                top_loop = loops.pop()
            else:
                raise Exception("secuencia mal formada: instruccion return sin loop asociado")

            p = ExperimentSecuence._get_pattern(pulsos=lsb + msb, freq=freq, phase=phase, freq_dirs=freq_dirs,
                                                phase_dirs=phase_dirs)
            data = top_loop["data"]
            lazo = top_loop["lazo"]
            secuence.retl(p, data, lazo, time_cp)
            ins += 1
            # ctualizamos demora al loop
            top_loop["demora"] += time_cp

            if loops:
                container_loop = loops.pop()
                container_loop["demora"] += ((top_loop["demora"]) * top_loop["rep"])
                loops.append(container_loop)
            else:
                demora += ((top_loop["demora"]) * top_loop["rep"])
            counter += 1
            return ExperimentSecuence._translate(cpoints, secuence, demora, counter, ins, loops, freq_dirs, phase_dirs)

        if cpoints[counter]["type"] == "L":
            n = cpoints[counter]["data"]
            lazo = len(loops)
            loops.append({"data": ins, "lazo": lazo, "demora": time_cp, "rep": n})
            p = ExperimentSecuence._get_pattern(pulsos=lsb + msb, freq=freq, phase=phase,
                                                freq_dirs=freq_dirs, phase_dirs=phase_dirs)
            secuence.lazo(p, n, lazo, demora)
            ins += 1
            counter += 1
            return ExperimentSecuence._translate(cpoints, secuence, demora, counter, ins, loops, freq_dirs, phase_dirs)

    @staticmethod
    def _get_pattern(pulsos, freq, phase, freq_dirs, phase_dirs, load_ram="0", udclk="0", disparo_ad=None):
        # 14 13 12 11 direccionamiento de fases
        # 10 udclk
        # 9 load ram
        # 8 direccionamiento de frecuencias
        # 5 disparo del AD

        p = phase_dirs[phase]
        p_1 = "0" * (4 - len("{0:b}".format(p))) + "{0:b}".format(p)

        f = freq_dirs[freq]
        f_1 = "0" * (1 - len("{0:b}".format(f))) + "{0:b}".format(f)

        # (16 15)-(14 13 12 11)-(10)-(9)-(8)-(7 6)-(5)-(4  3  2  1)
        # a  b    c  d  e  f    g    h   i   j k   l   m  n  o  p
        # 0  1    2  3  4  5    6    7   8   9 10  11  12 13 14 15

        s = pulsos[0:2] + p_1 + udclk + load_ram + f_1 + pulsos[9:16]

        if disparo_ad is not None:
            s = pulsos[0:2] + p_1 + udclk + load_ram + f_1 + pulsos[9:11] + disparo_ad + pulsos[12:16]

        return s
