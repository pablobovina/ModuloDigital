#!/usr/bin/python
# -*- coding: utf-8 -*-

from dds2 import Dds2
from ad import Ad
from pp2 import Pp2
from secuence import Secuence
import csv


def main():

    id_exp = "prueba piloto"
    # nombre del experimento

    freq = 2 * (10 ** 6)
    # numero entre 1 y 200 millones
    # max 200Mhz

    phase = 0
    # numero entre 0 y 360

    delta = 25
    # unidades en nsec 25 * 40 = 1000ns = 10us
    # numero entre 6 y 4294967295L == 2**32-1
    # base 40ns
    # 1000ns == 10us
    # 1000/40 == 25

    n_bloqs = 16
    # 64 * X
    # X = { 16, 32, 64 ... 128}
    # numero de muestras

    ts = 1000000
    # numero de muestras por segundo

    channel = 2
    # seleccion de canal
    # 0 a
    # 1 b
    # 2 a y b

    # creo secuencia solo adquisicion
    pulse_secuence = Secuence(id_exp)
    pattern = '0000000000010000'
    pulse_secuence.cont(pattern, delta)
    pulse_secuence.end()
    # cargo secuencia
    u_pp2 = Pp2(delay=0, secuence=pulse_secuence)
    u_pp2.upload_program()
    # configuro frecuencia y fase
    u_dds2 = Dds2(delay=0)
    u_dds2.reset()
    u_dds2.deactivate()
    u_dds2.freq(freq)
    u_dds2.phase(phase)
    u_dds2.activate()
    # configuro el AD
    u_ad = Ad(delay=0, bloqnum=n_bloqs, inter_ts=ts, channel=2)
    # disparo secuencia de pulsos
    u_pp2.trigger_program()
    # obtengo datos de los canales del AD
    u_ad.read_channels()

    return u_ad.data_a, u_ad.data_b


if __name__ == '__main__':
    data_a, data_b = main()

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
