#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modulo de control del AD
"""

from Usb import Usb
from time import sleep
import logging

logger = logging.getLogger("modDig")


class Ad(object):
    """clase para controlar el AD"""
    bloq_base = {1: 0x00, 2: 0x10, 4: 0x20, 8: 0x30, 16: 0x40, 32: 0x50, 64: 0x60, 128: 0x70}

    def __init__(self, mod_id=1, delay=0, amount=200, bloqnum=16, inter_ts=100):
        """
            id: entero, identificador de la instancia de dds2
            delay: en milisegundos, intervalo de tiempo entre comandos
        """
        errors = []
        self._check_mod_id(mod_id, errors)
        self._check_delay(delay, errors)
        self._check_amount(amount, errors)
        self._check_block_num(bloqnum, errors)
        self._check_inter_ts(inter_ts, errors)

        if errors:
            for error in errors:
                logger.error(error)
            raise Exception("error create instance AD " + ";".join(errors))

        self.mod_id = mod_id
        self.cmd = []
        self.delay = delay
        self.channel_a = None
        self.channel_b = None
        self.channel_ab = None
        self.data_a = None
        self.data_b = None
        self.buffer_len = bloqnum * 1024
        self.bloqnum = self.bloq_base.get(bloqnum, 0x00)
        self.inter_ts = inter_ts
        self.amount = amount
        self.interfaz = Usb()
        self._configure()

    @staticmethod
    def _check_mod_id(mod_id, errors=None):
        if not (mod_id > 0 and isinstance(mod_id, int)):
            errors.append("mod_id debe ser un numero entero mayor a 0")
        return

    @staticmethod
    def _check_delay(delay, errors=None):
        if not (0 <= delay <= 1000 and isinstance(delay, int)):
            errors.append("delay debe ser un entero en [0,1000]")
        return

    @staticmethod
    def _check_amount(amount, errors=None):
        if not (0 <= amount <= 500 and isinstance(amount, int)):
            errors.append("amount debe ser un entero en [0,500]")
        return

    @staticmethod
    def _check_block_num(bloqnum, errors=None):
        if bloqnum not in Ad.bloq_base.keys():
            errors.append("bloqnum debe estar en {}".format(Ad.bloq_base.keys()))
        return

    @staticmethod
    def _check_inter_ts(inter_ts, errors=None):
        if not (100 <= inter_ts <= 25400 and isinstance(inter_ts, int)):
            errors.append("inter_ts debe entero en nanosegundos [100, 25400]")
        return

    def _configure(self):
        self._reset10()
        self._reset01()
        self._set_time()
        self._execute()
        return

    def read_channels(self):
        self._reset10()
        self._reset00()
        self._execute()
        self.channel_b = self._leer(0x08)
        self._reset10()
        self._reset00()
        self._execute()
        self.channel_a = self._leer(0x0A)
        self._reset10()
        self._reset00()
        self._execute()
        self.channel_ab = self._leer(0x09)
        self.data_a, self.data_b = self._combinar(self.channel_b, self.channel_a, self.channel_ab)
        return

    def _reset10(self):
        # reset = 1  modoPC
        config = self.bloqnum
        config = config | 0x02
        config = config | 0x80
        config = config & 0xfe
        data = ['r', chr(0x0b), chr(config)]
        self.cmd.append((data, 4))
        return

    def _reset01(self):
        # ADSetConfig(mAdq, CmbBarrido->ItemIndex, 0, 1);
        config = self.bloqnum
        config = config | 0x02
        config = config & 0x7f
        config = config | 0x01
        data = ['r', chr(0x0b), chr(config)]
        self.cmd.append((data, 4))
        return

    def _reset00(self):
        # ADSetConfig(mAdq, CmbBarrido->ItemIndex, 0, 0);
        config = self.bloqnum
        config = config | 0x02
        config = config & 0x7f
        config = config & 0xfe
        data = ['r', chr(0x0b), chr(config)]
        self.cmd.append((data, 4))
        return

    def _set_time(self):
        muestras = self.inter_ts / 100.
        delta_t = 255 - int(muestras)
        data = ['t', chr(0x0c), chr(delta_t)]
        self.cmd.append((data, 4))
        return

    def _leer(self, channel_dir):
        data = ['B', chr(channel_dir)]
        self.interfaz.request_write(data)
        response = self.interfaz.request_read(self.buffer_len)
        return response

    def _completar(self, s):
        if len(s) != self.buffer_len:
            for _ in range(self.buffer_len - len(s)):
                s += chr(0x00)
        return s

    def _combinar(self, l1, l2, l3):

        max_len = max(len(l1), len(l2), len(l3))
        l1 = self._completar(l1)
        l2 = self._completar(l2)
        l3 = self._completar(l3)
        ca = []
        cb = []

        # usb.CanalB[i] = ((usb.Canal3[i]) & 0x0f) + (usb.Canal1[i] * 16);
        # usb.CanalA[i] = ((usb.Canal3[i] / 16) & 0x0f) + ((usb.Canal2[i]) * 16);
        for i in range(max_len):
                ca.append((i, (ord(l3[i]) & 0x0F) + ord(l1[i]) * 16))
                cb.append((i, (ord(l3[i])/16) & 0x0F + ord(l2[i]) * 16))
        return ca, cb

    def _execute(self):
        """ejecutar pila de instucciones del ad"""
        data = self.interfaz.execute(self.delay, self.cmd)
        self.cmd = []
        return data
