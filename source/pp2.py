#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modulo de control del PP2
"""

from Usb import Usb
from time import sleep
import logging

logger = logging.getLogger("__main__")


class Pp2(object):
    """clase para controlar el pp2"""

    def __init__(self, mod_id=1, delay=0, amount=200):
        """
            id: entero, identificador de la instancia de dds2
            delay: en milisegundos, intervalo de tiempo entre comandos
        """
        errors = []
        self._check_mod_id(mod_id, errors)
        self._check_delay(delay, errors)
        self._check_amount(amount, errors)
        if errors:
            for error in errors:
                logger.error(error)
            raise Exception("error create instance PP2 " + ";".join(errors))

        self.mod_id = mod_id
        self.cmd = []
        self.delay = delay
        self.secuence = None
        self.interfaz = Usb()
        self.amount = amount

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

    def upload_program(self, s):
        self.secuence = s
        if self.secuence.empty():
            logging.error("Intenta ejecutar una secuencia de pulsos vacia")
            raise Exception("Intenta ejecutar una secuencia de pulsos vacia")
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
        return True

    def trigger_program(self):
        # instruccion disparo de secuencia de pulsos
        self.cmd.append((['M', chr(0x50), chr(0x00)], 4))
        self.cmd.append((['D', chr(0x50), chr(0x00), chr(0x80)], 4))
        self._execute()
        return True

    def _execute(self):
        """ejecutar pila de instucciones del pp2"""
        data = self.interfaz.execute(self.delay, self.cmd)
        self.cmd = []
        return data

    def wait_end_run(self):
        """generalizar usando execute until"""
        intentos = 0
        flag = False

        if self.interfaz.debug:
            return True

        op = ['E', chr(0x50), chr(0x00)]
        while intentos < self.amount:
            response = self.interfaz.request(op, 4)
            if ord(response.value[0]) & 0x01:
                flag = True
                break
            else:
                intentos += 1
                sleep(self.delay)
        return flag
