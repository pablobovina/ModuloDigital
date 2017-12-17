#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modulo de control del DDS2
"""

from Usb import Usb


class Dds2(object):
    """clase para controlar el dds2"""

    # codigos de estados del dds2
    op_codes = {"execute": 1, "on": 2, "reset": 3, "off": 4, "freq": 5, "phase": 6}

    def __init__(self, mod_id=1, delay=5):
        """
            id: entero, identificador de la instancia de dds2
            delay: en milisegundos, intervalo de tiempo entre comandos
        """
        self.mod_id = mod_id
        self.last_request = None
        self.requested_operations = []
        self.status = None
        self.cmd = []
        self.delay = delay
        self.interfaz = Usb()

    def reset(self):
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
        
        print "dds2 reset"
        self.requested_operations.append(self.op_codes['reset'])
        self.last_request = self.op_codes['reset']
        self.status = self.op_codes['reset']

        return True

    def activate(self):
        """activar el dds2"""

        # modo PC
        self.cmd.append((['b', chr(0x71), chr(0x00)], 4))
        # cargar dds2 con 0x10
        self.cmd.append((['k', chr(0x75), chr(0x1d), chr(0x78), chr(0x10)], 4))
        # modo dds con fases
        self.cmd.append((['b', chr(0x71), chr(0x05)], 4))
        self._execute()

        print "dds2 on"
        self.requested_operations.append(self.op_codes['on'])
        self.last_request = self.op_codes['on']
        self.status = self.op_codes['on']

        return True

    def deactivate(self):
        """desactivar el dds2"""

        # modo PC
        self.cmd.append((['b', chr(0x71), chr(0x00)], 4))
        # cargar un registro 1d del DDS2 con 0x17
        self.cmd.append((['k', chr(0x75), chr(0x1d), chr(0x78), chr(0x17)], 4))
        # pulso UDCLK
        self.cmd.append((['u', chr(0x76), chr(0x00)], 4))
        self._execute()

        print "dds2 off"
        self.requested_operations.append(self.op_codes['off'])
        self.last_request = self.op_codes['off']
        self.status = self.op_codes['off']
        return True

    def freq(self, f):
        """configurar frecuencia de trabajo"""

        calculo = f * 281474976710656 / 200000000
        w1_5 = calculo / 1099511627776
        calculo = calculo - (w1_5 * 1099511627776)
        w1_4 = calculo / 4294967296
        calculo = calculo - (w1_4 * 4294967296)
        w1_3 = calculo / 16777216
        calculo = calculo - (w1_3 * 16777216)
        w1_2 = calculo / 65536
        calculo = calculo - (w1_2 * 65536)
        w1_1 = calculo / 256
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
        #self.cmd.append((['u', chr(0x76), chr(0x00)], 4))
        self._execute()

        print "dds2 set freq"
        self.requested_operations.append(self.op_codes['freq'])
        self.last_request = self.op_codes['freq']
        self.status = self.op_codes['freq']

        return True

    def phase(self, p):
        """configurar fase de trabajo"""
        fs1_h = p / 256
        fs1_l = p - (fs1_h * 256)

        # modo escritura de ram de fases
        self.cmd.append((['b', chr(0x71), chr(0x02)], 4))
        # set ram con fase
        self.cmd.append((['w', chr(0x70), chr(0x00), chr(0x74), chr(fs1_h),
                          chr(0x70), chr(0x01), chr(0x74), chr(fs1_l)], 4))
        # modo PC
        self.cmd.append((['b', chr(0x71), chr(0x00)], 4))
        self._execute()

        print "dds2 set phase"
        self.requested_operations.append(self.op_codes['phase'])
        self.last_request = self.op_codes['phase']
        self.status = self.op_codes['phase']

        return True

    def _execute(self):
        """ejecutar pila de instucciones del dds2"""

        data = self.interfaz.execute(self.delay, self.cmd)

        print "dds2 execute"
        self.requested_operations = []
        self.last_request = self.op_codes['execute']
        self.status = self.op_codes['execute']
        return data
