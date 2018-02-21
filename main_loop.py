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

    freq = 8 * (10 ** 6)
    # numero entre 1 y 200 millones
    # max 200Mhz

    phase = 0
    # numero entre 0 y 360

    delta = 10000
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

    pulse_secuence = Secuence(id_exp)

    #loop1
    pattern = '0000000000000001'
    pulse_secuence.lazo(pattern, 10, 1)
    pattern = '0000000000000001'
    pulse_secuence.cont(pattern, delta)
    pattern = '0000000000000001'
    pulse_secuence.retl(pattern, 0)
    #salida fija
    pattern = '0000000000000010'
    pulse_secuence.cont(pattern, delta)
    #loop2
    pattern = '0000000000000011'
    pulse_secuence.lazo(pattern, 10, 1)
    pattern = '0000000000000011'
    pulse_secuence.cont(pattern, delta)
    pattern = '0000000000000011'
    pulse_secuence.retl(pattern, 4)
    # creo secuencia solo adquisicion
    # pulso 9
    pattern = '0000000100000000'
    pulse_secuence.cont(pattern, delta)
    # pulso 10
    pattern = '0000001000000000'
    pulse_secuence.cont(pattern, delta)
    #pulso 5 y 16 para cerrar llave
    pattern = '1000000000010000'
    pulse_secuence.cont(pattern, delta)
    #fin
    pulse_secuence.end()
    # cargo secuencia
    u_pp2 = Pp2(delay=0, secuence=pulse_secuence)
    u_pp2.upload_program()
    # configuro frecuencia y fase
    u_dds2 = Dds2(delay=0)
    u_dds2.reset()
    u_dds2.freq(freq)
    u_dds2.phase(phase)
    print "activamos DDS2"
    u_dds2.activate()
    # configuro el AD
    u_ad = Ad(delay=0, bloqnum=n_bloqs, inter_ts=ts, channel=2)
    u_ad.configure()
    # disparo secuencia de pulsos
    print "disparamos programa PP2"
    u_pp2.trigger_program()
    # obtengo datos de los canales del AD
    u_ad.read_channels()
    sleep(5)
    print "desctivo DDS2"
    u_dds2.deactivate()
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
