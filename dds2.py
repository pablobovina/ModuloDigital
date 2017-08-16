"""
Modulo de control del DDS2
"""


class dds2(object):
    """clase para controlar el dds2"""

    op_codes = {'master_reset': 0}

    def __init__(self, id=1):
        self.id = id
        self.last_request = None
        self.requested_operations = []

    def reset_dds2(self):
        """lista de comandos para un master reset de dds2"""

        cmd = []

        # b 71 00
        # pasar a modo PC  (registro de comando 2)
        cmd.append(['b', chr(0x71), chr(0x00)])

        # resetear y desactivar el DDS
        # Master RESET
        # a 72 00
        # pulso de RESET (registro de comando 3)
        cmd.append(['a', chr(0x72), chr(0x00)])

        # configurar el DDS
        # cargar un registro 1f del DDS2 con 02
        # k 75 1f 78 02
        cmd.append(['k', chr(0x75), chr(0x1f), chr(0x78), chr(0x02)])

        # cargar un registro 1d del DDS2 con 0x17
        # k 75 1d 78 17
        cmd.append(['k', chr(0x75), chr(0x1d), chr(0x78), chr(0x17)])

        # cargar un registro 1e del DDS2 con 0x44
        # k 75 1e 78 44
        # PLL out. 0x44 = 200Mhz, 0x45 = 250Mhz, 0x46 = 300Mhz
        cmd.append(['k', chr(0x75), chr(0x1e), chr(0x78), chr(0x44)])

        # cargar un registro 20 del DDS2 con 00
        # k 75 20 78 00
        # Shape keying deshabilitado
        cmd.append(['k', chr(0x75), chr(0x20), chr(0x78), chr(0x00)])
        
        print "dds2 desactivado"
        self.requested_operations.append(self.op_codes['master_reset'])
        self.last_request = self.op_codes['master_reset']

        return cmd