#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modulo de definicion de secuencias aceptados
"""
from textwrap import wrap
import logging

logger = logging.getLogger("__main__")

class Secuence(object):
    """clase para generar secuencias"""

    def __init__(self, sec_name="test1"):
        self.sec_name = sec_name
        self.instructions = []

    def cont(self, pattern, demora):
        # print "continue " + pattern + " " + str(demora)
        logger.info("continue " + pattern + " " + str(demora))
        t = "0" * (32 - len("{0:b}".format(demora))) + "{0:b}".format(demora)
        ins = wrap(pattern + "0" * 11 + "0" * 2 + "001" + t, 8)
        ins.reverse()
        self.instructions.append(ins)
        return True

    def end(self):
        # print "fin"
        logger.info("fin")
        ins = wrap("0" * 16 + "0" * 11 + "0" * 2 + "111" + "0" * 32, 8)
        ins.reverse()
        self.instructions.append(ins)
        return True

    def lazo(self, pattern, data, lazo, demora):
        # print "lazo " + pattern + " " + str(data) + " " + str(lazo) + " " + str(demora)
        logger.info("lazo " + pattern + " " + str(data) + " " + str(lazo) + " " + str(demora))
        d = "0" * (11 - len("{0:b}".format(data))) + "{0:b}".format(data)
        t = "0" * (32 - len("{0:b}".format(demora))) + "{0:b}".format(demora)
        l = "0" * (2 - len("{0:b}".format(lazo))) + "{0:b}".format(lazo)
        ins = wrap(pattern + d + l + "010" + t, 8)
        ins.reverse()
        self.instructions.append(ins)
        return True

    def retl(self, pattern, data, lazo, demora):
        # print "retl " + pattern + " " + str(data) + " " + str(lazo) + " " + str(demora)
        logger.info("retl " + pattern + " " + str(data) + " " + str(lazo) + " " + str(demora))
        d = "0" * (11 - len("{0:b}".format(data))) + "{0:b}".format(data)
        t = "0" * (32 - len("{0:b}".format(demora))) + "{0:b}".format(demora)
        l = "0" * (2 - len("{0:b}".format(lazo))) + "{0:b}".format(lazo)
        ins = wrap(pattern + d + l + "011" + t, 8)
        ins.reverse()
        self.instructions.append(ins)
        return True

    def empty(self):
        return len(self.instructions) == 0
