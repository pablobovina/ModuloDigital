#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modulo de control del AD
"""

from Usb import Usb
from time import sleep


class Ad(object):
    """clase para controlar el AD"""

    # codigos de estados del pp2
    op_codes = {"execute": 1, "reset": 2, "setTime": 3, "configure": 4, "loaded": 5,
                "canalB": 8, "canalA": 9, "canalAB": 10}
    channels = {0x08: "canalB", 0x0A: "canalA", 0x09: "canalAB"}
    bloq_base = {16: 0x00, 32: 0x10, 64: 0x20, 128: 0x30, 256: 0x40, 512: 0x50, 1024: 0x60, 2048: 0x70}

    def __init__(self, mod_id=1, delay=5, amount=200,  bloqnum=16, inter_ts=1000000, channel=2):
        """
            id: entero, identificador de la instancia de dds2
            delay: en milisegundos, intervalo de tiempo entre comandos
        """
        self.mod_id = mod_id
        self.last_request = None
        self.requested_operations = []
        self.cmd = []
        self.history = []
        self.status = None
        self.delay = delay
        self.channel = channel
        self.channel_a = None
        self.channel_b = None
        self.channel_ab = None
        self.data_a = None
        self.data_b = None
        self.buffer_len = bloqnum * 64
        self.bloqnum = self.bloq_base.get(bloqnum, 0x00)
        self.inter_ts = inter_ts
        self.amount = amount
        self.interfaz = Usb()

    def configure(self):
        self._reset10()
        self._reset01()
        self._set_time()
        self._execute()
        print "ad configured"
        self.history.append(self.op_codes['configure'])
        self.last_request = self.op_codes['configure']
        self.status = self.op_codes['configure']

    def read_channels(self):
        flag = self._wait_convertion()
        print "finalizo la conversion con estado: " + str(flag)
        self._reset10()
        self._reset00()
        self._leer(0x08)  # B Canal1
        self.channel_b = self._execute().pop()
        self._reset10()
        self._reset00()
        self._leer(0x0A)  # A Canal2
        self.channel_a = self._execute().pop()
        self._reset10()
        self._reset00()
        self._leer(0x09)  # AB Canal3
        self.channel_ab = self._execute().pop()
        self.data_a, self.data_b = self._combinar(self.channel_b, self.channel_a, self.channel_ab)

        print "ad cargado con datos"
        self.history.append(self.op_codes['loaded'])
        self.last_request = self.op_codes['loaded']
        self.status = self.op_codes['loaded']

    def _reset10(self):
        # reset = 1  modoPC
        config = self.bloqnum
        config = config | 0x02
        config = config | 0x80
        config = config & 0xfe
        data = ['r', chr(0x0b), chr(config)]
        self.cmd.append((data, 4))

        print "AD reset10"
        self.requested_operations.append(self.op_codes['reset'])
        self.last_request = self.op_codes['reset']
        self.status = self.op_codes['reset']

    def _reset01(self):
        # ADSetConfig(mAdq, CmbBarrido->ItemIndex, 0, 1);
        config = self.bloqnum
        config = config | 0x02
        config = config & 0x7f
        config = config | 0x01
        data = ['r', chr(0x0b), chr(config)]
        self.cmd.append((data, 4))

        print "AD reset01"
        self.requested_operations.append(self.op_codes['reset'])
        self.last_request = self.op_codes['reset']
        self.status = self.op_codes['reset']

    def _reset00(self):
        # ADSetConfig(mAdq, CmbBarrido->ItemIndex, 0, 0);
        config = self.bloqnum
        config = config | 0x02
        config = config & 0x7f
        config = config & 0xfe
        data = ['r', chr(0x0b), chr(config)]
        self.cmd.append((data, 4))

        print "AD reset00"
        self.requested_operations.append(self.op_codes['reset'])
        self.last_request = self.op_codes['reset']
        self.status = self.op_codes['reset']

    def _set_time(self):
        if self.inter_ts * .0000001 != 0:
            muestras = 1. / (self.inter_ts * .0000001)
            delta_t = 255 - int(muestras)
            data = ['t', chr(0x0c), chr(delta_t)]
            self.cmd.append((data, 4))

            print "set_time"
            self.requested_operations.append(self.op_codes['setTime'])
            self.last_request = self.op_codes['setTime']
            self.status = self.op_codes['setTime']

    def _leer(self, channel_dir):
        data = ['B', chr(channel_dir)]
        self.cmd.append((data, self.buffer_len))

        print "AD leer canal " + self.channels[channel_dir]
        op = self.op_codes[self.channels[channel_dir]]
        self.requested_operations.append(op)
        self.last_request = op
        self.status = op

    def _completar(self, s):
        if len(s) != self.buffer_len:
            for _ in range(self.buffer_len - len(s)):
                s += chr(0x00)
        return s

    def _combinar(self, l1, l2, l3):

        l = max(len(l1), len(l2), len(l3))
        l1 = self._completar(l1)
        l2 = self._completar(l2)
        l3 = self._completar(l3)
        print l
        ca = []
        cb = []

        # usb.CanalB[i] = ((usb.Canal3[i]) & 0x0f) + (usb.Canal1[i] * 16);
        # usb.CanalA[i] = ((usb.Canal3[i] / 16) & 0x0f) + ((usb.Canal2[i]) * 16);
        for i in range(l):
                ca.append((i, (ord(l3[i]) & 0x0F) + ord(l1[i]) * 16))
                cb.append((i, (ord(l3[i])/16) & 0x0F + ord(l2[i]) * 16))
        return ca, cb

    def _execute(self):
        """ejecutar pila de instucciones del AD"""
        data = self.interfaz.execute(self.delay, self.cmd)

        print "ad execute requested_operations"
        self.requested_operations.append(self.op_codes['execute'])
        self.last_request = self.op_codes['execute']
        self.status = self.op_codes['execute']
        return data

    def _wait_convertion(self):
        """generalizar usando execute until"""
        intentos = 0
        flag = False
        op = ['S', chr(0x0b), chr(0x00)]
        while intentos < self.amount:
            response = self.interfaz.request(op, 4)
            if ord(response.value[0]) & 0x01:
                intentos = self.amount
                flag = True
                print "caracter esperado para cortar"
                print response.value
                print ord(response.value[0])
            else:
                intentos += 1
                sleep(self.delay)
        return flag
