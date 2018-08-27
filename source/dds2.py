#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modulo de control del DDS2
"""

from Usb import Usb
import logging

logger = logging.getLogger("modDig")


class Dds2(object):
    """clase para controlar el dds2"""

    def __init__(self, freq, phase, mod_id=1, delay=0):
        """
            id: entero, identificador de la instancia de dds2
            delay: en milisegundos, intervalo de tiempo entre comandos
            :type freq: set
            :type phase: set
        """

        errors = []

        self._check_mod_id(mod_id, errors)
        self._check_delay(delay, errors)
        self._check_freq(freq, errors)
        self._check_phase(phase, errors)

        if errors:
            for error in errors:
                logger.error(error)
            raise Exception("error create instance DDS2 " + ";".join(errors))

        self.mod_id = mod_id
        self.cmd = []
        self.delay = delay
        self.interfaz = Usb()
        self.phase_table = {}
        self.freq_table = {}

        self._reset()

        f1 = freq.pop()
        self._freq1(f1)
        if len(freq):
            f2 = freq.pop()
            self._freq2(f2)

        counter_p = 0
        for p in phase:
            self._phase(p, counter_p)
            counter_p += 1
        self._activate()

        return

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
    def _check_freq(freq, errors=None):
        if not len(freq):
            errors.append("no hay frecuencias para almacenar")

        if not (1 <= len(freq) <= 2):
            errors.append("hay mas de 2 frecuencias para almacenar")

        for f in freq:
            if not (isinstance(f, int) and 0 <= f <= 200000000):
                errors.append("no se puede almacenar la frecuencia {} debe ser entero en [0,200000000]".format(f))

        return

    @staticmethod
    def _check_phase(phase, errors=None):

        if not len(phase):
            errors.append("no hay fases para almacenar")

        if not (1 <= len(phase) <= 16):
            errors.append("hay mas de 16 fases para almacenar")

        for p in phase:
            if not (isinstance(p, int) and 0 <= p <= 360):
                errors.append("no se puede almacenar la fase {} debe ser entero en [0,360]".format(p))

        return

    def _reset(self):
        """lista de comandos para un master reset de dds2"""

        # pasar a modo PC  (registro de comando 2)
        self.cmd.append((['b', chr(0x71), chr(0x00)], 4))
        # pulso de RESET (registro de comando 3)
        self.cmd.append((['a', chr(0x72), chr(0x00)], 4))
        # cargar un registro 1f del DDS2 con 02
        self.cmd.append((['k', chr(0x75), chr(0x1f), chr(0x78), chr(0x02)], 4))
        # cargar un registro 1d del DDS2 con 0x17
        self.cmd.append((['k', chr(0x75), chr(0x1d), chr(0x78), chr(0x17)], 4))
        # cargar un registro 1e del DDS2 con 0x44
        # PLL out. 0x44 = 200Mhz, 0x45 = 250Mhz, 0x46 = 300Mhz
        self.cmd.append((['k', chr(0x75), chr(0x1e), chr(0x78), chr(0x44)], 4))
        # cargar un registro 20 del DDS2 con 00
        # Shape keying deshabilitado
        self.cmd.append((['k', chr(0x75), chr(0x20), chr(0x78), chr(0x00)], 4))
        self._execute()
        return True

    def _activate(self):
        """activar el dds2"""

        # modo PC
        self.cmd.append((['b', chr(0x71), chr(0x00)], 4))
        # cargar dds2 con 0x10
        self.cmd.append((['k', chr(0x75), chr(0x1d), chr(0x78), chr(0x10)], 4))
        # modo dds con fases
        self.cmd.append((['b', chr(0x71), chr(0x05)], 4))
        self._execute()
        return True

    def _deactivate(self):
        """desactivar el dds2"""

        # modo PC
        self.cmd.append((['b', chr(0x71), chr(0x00)], 4))
        # cargar un registro 1d del DDS2 con 0x17
        self.cmd.append((['k', chr(0x75), chr(0x1d), chr(0x78), chr(0x17)], 4))
        # pulso UDCLK
        self.cmd.append((['u', chr(0x76), chr(0x00)], 4))
        self._execute()
        return True

    def _freq1(self, f1):
        """configurar frecuencia de trabajo"""

        calculo = f1 * ((2**48)-1) / 200000000
        w1_5 = calculo / (2**40)
        calculo = calculo - (w1_5 * 1099511627776)
        w1_4 = calculo / (2**32)
        calculo = calculo - (w1_4 * 4294967296)
        w1_3 = calculo / (2**24)
        calculo = calculo - (w1_3 * 16777216)
        w1_2 = calculo / (2**16)
        calculo = calculo - (w1_2 * 65536)
        w1_1 = calculo / (2**8)
        w1_0 = calculo - (w1_1 * 256)

        # modo PC
        self.cmd.append((['b', chr(0x71), chr(0x00)], 4))
        # set registros de frecuencia
        self.cmd.append((['k', chr(0x75), chr(0x04), chr(0x78), chr(w1_5)], 4))
        self.cmd.append((['k', chr(0x75), chr(0x05), chr(0x78), chr(w1_4)], 4))
        self.cmd.append((['k', chr(0x75), chr(0x06), chr(0x78), chr(w1_3)], 4))
        self.cmd.append((['k', chr(0x75), chr(0x07), chr(0x78), chr(w1_2)], 4))
        self.cmd.append((['k', chr(0x75), chr(0x08), chr(0x78), chr(w1_1)], 4))
        self.cmd.append((['k', chr(0x75), chr(0x09), chr(0x78), chr(w1_0)], 4))
        # pulso UDCLK actualiza registro de trabajo
        self.cmd.append((['u', chr(0x76), chr(0x00)], 4))
        self._execute()
        self.freq_table[f1] = 0
        return True

    def _freq2(self, f2):
        """configurar frecuencia de trabajo"""

        calculo = f2 * ((2 ** 48) - 1) / 200000000
        w1_5 = calculo / (2 ** 40)
        calculo = calculo - (w1_5 * 1099511627776)
        w1_4 = calculo / (2 ** 32)
        calculo = calculo - (w1_4 * 4294967296)
        w1_3 = calculo / (2 ** 24)
        calculo = calculo - (w1_3 * 16777216)
        w1_2 = calculo / (2 ** 16)
        calculo = calculo - (w1_2 * 65536)
        w1_1 = calculo / (2 ** 8)
        w1_0 = calculo - (w1_1 * 256)

        # modo PC
        self.cmd.append((['b', chr(0x71), chr(0x00)], 4))
        # set registros de frecuencia
        self.cmd.append((['k', chr(0x75), chr(0x0a), chr(0x78), chr(w1_5)], 4))
        self.cmd.append((['k', chr(0x75), chr(0x0b), chr(0x78), chr(w1_4)], 4))
        self.cmd.append((['k', chr(0x75), chr(0x0c), chr(0x78), chr(w1_3)], 4))
        self.cmd.append((['k', chr(0x75), chr(0x0d), chr(0x78), chr(w1_2)], 4))
        self.cmd.append((['k', chr(0x75), chr(0x0e), chr(0x78), chr(w1_1)], 4))
        self.cmd.append((['k', chr(0x75), chr(0x0f), chr(0x78), chr(w1_0)], 4))
        # pulso UDCLK actualiza registro de trabajo
        self.cmd.append((['u', chr(0x76), chr(0x00)], 4))
        self._execute()
        self.freq_table[f2] = 1

        return True

    def _phase(self, p, d):
        """configurar fase de trabajo"""
        # resolucion es  2 ** 14 / 360 resolucion
        fs1_h = (45 * p) / 256
        fs1_l = (45 * p) - (fs1_h * 256)

        # modo escritura de ram de fases
        self.cmd.append((['b', chr(0x71), chr(0x02)], 4))
        # set ram con fase
        self.cmd.append((['w', chr(0x70), chr(d*2), chr(0x74), chr(fs1_h),
                          chr(0x70), chr((d*2)+1), chr(0x74), chr(fs1_l)], 4))
        # modo PC
        self.cmd.append((['b', chr(0x71), chr(0x00)], 4))
        self._execute()
        self.phase_table[p] = d
        return True

    def _execute(self):
        """ejecutar pila de instucciones del dds2"""
        data = self.interfaz.execute(self.delay, self.cmd)
        # limpio comandos a enviar
        self.cmd = []
        return data
