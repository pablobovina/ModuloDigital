#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modulo de definicion de secuencias aceptados
"""
from textwrap import wrap


class Secuence(object):
    """clase para generar secuencias"""

    def __init__(self, sec_name="test1"):
        self.sec_name = sec_name
        self.instructions = []

    def cont(self, pattern, t):
        print "continue " + pattern + " " + str(t)
        t = "0" * (32 - len("{0:b}".format(t))) + "{0:b}".format(t)
        ins = wrap(pattern + "0"*11 + "0"*2 + "001" + t, 8)
        ins.reverse()
        self.instructions.append(ins)
        return True

    def end(self):
        print "fin"
        ins = wrap("0" * 16 + "0" * 11 + "0" * 2 + "111" + "0"*32, 8)
        ins.reverse()
        self.instructions.append(ins)
        return True
