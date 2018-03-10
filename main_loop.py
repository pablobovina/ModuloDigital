#!/usr/bin/python
# -*- coding: utf-8 -*-

from dds2 import Dds2
from ad import Ad
from pp2 import Pp2
from secuence import Secuence
import csv
from time import sleep


def main():

    id_exp = "prueba piloto"
    # nombre del experimento

    delta = 4000000
    delta_1 = 40000000
    # unidades en nsec 25 * 40 = 1000ns = 10us
    # numero entre 6 y 4294967295L == 2**32-1
    # base 40ns
    # 1000ns == 10us
    # 1000/40 == 25

    pulse_secuence = Secuence(id_exp)
    pattern_1 = "1" * 16
    pattern_0 = "0" * 16
    pulse_secuence.lazo(pattern_0, 5, 0, 23)
    pulse_secuence.cont(pattern_0, delta)
    pulse_secuence.cont(pattern_1, delta)
    pulse_secuence.retl(pattern_0, 0, 0, 23)
    pulse_secuence.cont(pattern_0, delta_1)
    pulse_secuence.lazo(pattern_0, 2, 0, 23)
    pulse_secuence.cont(pattern_0, delta)
    pulse_secuence.cont(pattern_1, delta)
    pulse_secuence.retl(pattern_0, 5, 0, 23)

    pulse_secuence.end()
    # cargo secuencia
    u_pp2 = Pp2(delay=0, secuence=pulse_secuence)
    u_pp2.upload_program()
    # disparo secuencia de pulsos
    print "disparamos programa PP2"
    u_pp2.trigger_program()
    # obtengo datos de los canales del AD
    return

if __name__ == '__main__':
    main()

