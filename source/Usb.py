# -*- coding: utf-8 -*-
import ctypes
from time import sleep
import logging
from setup import SetupModDig

logger = logging.getLogger("modDig")


class Usb:
    vid = "vid_04d8&pid_000c"
    out_pipe = "\\MCHP_EP1"
    in_pipe = "\\MCHP_EP1"
    selection = 0
    write_delay = 5
    read_delay = 5
    api = None
    debug = False

    def __init__(self):
        self.debug = SetupModDig.debug
        Usb.debug = SetupModDig.debug
        if not self.debug:
            self.api = ctypes.CDLL("C:\\Users\\pablo\\Downloads\\tesis\\repo\\ServerModuloDigital\\Server\\experiments\\ModuloDigital\\Microchip\\mpusbapi.dll")
            # self.api = ctypes.CDLL(".\\Microchip\\mpusbapi.dll")

    def request_fake(self, data, data_len):
        return chr(0x00)*data_len

    def execute(self, delay, requests):
        """ejecutar pila de instucciones del AD"""
        data = []
        for c in requests:
            if self.debug:
                response = self.request_fake(*c)
                data.append(response)
            else:
                command = c[0]
                comand_len = c[1]
                self.request_write(command)
                response = self.request_read(comand_len)
                data.append(response.value)

            sleep(delay)
        return data

    def request_read(self, data_len):
        
        if self.debug:
            return self.request_fake("", data_len)

        if not self.api._MPUSBGetDeviceCount(self.vid):
            raise Exception("Modulo desconectado")
        pout = self.api._MPUSBOpen(self.selection, self.vid, self.out_pipe, 0, 0)
        pin = self.api._MPUSBOpen(self.selection, self.vid, self.in_pipe, 1, 0)

        receive_data = ctypes.create_string_buffer(data_len)
        receive_length = (ctypes.c_ulong * 1)()
        ctypes.cast(receive_length, ctypes.POINTER(ctypes.c_ulong))
        receive_delay = self.read_delay
        expected_receive_length = data_len

        self.api._MPUSBRead(pin, receive_data, expected_receive_length, receive_length, receive_delay)
        self.api._MPUSBClose(pin)
        self.api._MPUSBClose(pout)

        return receive_data

    def request_write(self, data):
        """
        make a request to module microchip via usb
        data: data to write
        data_len: number of bytes incoming in response
        """

        if self.debug:
            return True

        if not self.api._MPUSBGetDeviceCount(self.vid):
            raise Exception("Modulo desconectado")
        
        pout = self.api._MPUSBOpen(self.selection, self.vid, self.out_pipe, 0, 0)
        pin = self.api._MPUSBOpen(self.selection, self.vid, self.in_pipe, 1, 0)

        data = "".join(data)
        send_data = ctypes.create_string_buffer(data)
        sent_data_lenght = (ctypes.c_ulong * 1)()
        ctypes.cast(sent_data_lenght, ctypes.POINTER(ctypes.c_ulong))
        send_delay = self.write_delay
        send_lenght = len(data)

        self.api._MPUSBWrite(pout, send_data, send_lenght, sent_data_lenght, send_delay)
        self.api._MPUSBClose(pin)
        self.api._MPUSBClose(pout)

        return True
