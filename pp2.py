#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modulo de control del PP2
"""

from Usb import Usb
from secuence import Secuence
from time import sleep

class Pp2(object):
    """clase para controlar el pp2"""

    # codigos de estados del pp2
    op_codes = {"execute": 1, "on": 2, "reset": 3, "off": 4, "upload": 5, "trigger": 6}

    def __init__(self, mod_id=1, delay=5, amount=200):
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
        self.secuence = None
        self.interfaz = Usb()
        self.amount = amount

    def upload_program(self, s):
        self.secuence = s
        # reset pp2
        self.cmd.append((['R', chr(0x50), chr(0x02)], 4))
        # modo carga
        self.cmd.append((['c', chr(0x50), chr(0x03)], 4))
        # comandos de transferencia

        for c in self.secuence.instructions:
            instruction = ['A', chr(0x51)]
            for b in c:
                instruction.append(chr(int(b, 2)))
            self.cmd.append((instruction, 4))
            self.cmd.append((['T', chr(0x52), chr(0x00)], 4))

        self._execute()

        print "pp2 upload program"
        self.requested_operations.append(self.op_codes['upload'])
        self.last_request = self.op_codes['upload']
        self.status = self.op_codes['upload']

        return True

    def trigger_program(self):

        # instruccion disparo de secuencia de pulsos
        self.cmd.append((['M', chr(0x50), chr(0x00)], 4))
        self.cmd.append((['D', chr(0x50), chr(0x00), chr(0x80)], 4))
        self._execute()

        print "pp2 trigger program"
        self.requested_operations.append(self.op_codes['trigger'])
        self.last_request = self.op_codes['trigger']
        self.status = self.op_codes['trigger']

        return True

    def _execute(self):
        """ejecutar pila de instucciones del pp2"""

        data = self.interfaz.execute(self.delay, self.cmd)

        #print "pp2 execute"
        self.requested_operations.append(self.op_codes['execute'])
        self.last_request = self.op_codes['execute']
        self.status = self.op_codes['execute']
        self.cmd = []
        return data

    def wait_end_run(self):
        """generalizar usando execute until"""
        intentos = 0
        flag = False
        op = ['E', chr(0x52), chr(0x00)]
        while intentos < self.amount:
            response = self.interfaz.request(op, 4)
            print response.value
            print "pp2 wait end run"
            if ord(response.value[0]) & 0x01:
                intentos = self.amount
                flag = True
                print "caracter esperado para cortar"
                print response.value
                print ord(response.value[0])
                break
            else:
                intentos += 1
                sleep(self.delay)
        return flag
