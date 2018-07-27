# -*- coding: utf-8 -*-
import ctypes
import logging
from time import sleep
from setup import USB_FAKE


class Usb:
    vid = "vid_04d8&pid_000c"
    out_pipe = "\\MCHP_EP1"
    in_pipe = "\\MCHP_EP1"
    api = ctypes.CDLL("C:\\Users\\pablo\\Downloads\\tesis\\repo\\ModuloDigital\\Microchip\\mpusbapi.dll")
    # api = ctypes.CDLL(".\\Microchip\\mpusbapi.dll")
    selection = 0
    write_delay = 600
    read_delay = 600
    debug = USB_FAKE

    def __init__(self, debug=False):
        #logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
        #                    level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')
        pass

    def request(self, data, data_len):
        """
        make a request to module microchip via usb
        data: data to write
        data_len: number of bytes incoming in response
        """
        if not self.api._MPUSBGetDeviceCount(self.vid):
            raise Exception("Modulo desconectado")
        pout = self.api._MPUSBOpen(self.selection, self.vid, self.out_pipe, 0, 0)
        pin = self.api._MPUSBOpen(self.selection, self.vid, self.in_pipe, 1, 0)

        data = "".join(data)
        #logging.info("join data "+data)
        send_data = ctypes.create_string_buffer(data)
        sent_data_lenght = (ctypes.c_ulong * 1)()
        ctypes.cast(sent_data_lenght, ctypes.POINTER(ctypes.c_ulong))
        send_delay = self.write_delay
        send_lenght = len(data)

        self.api._MPUSBWrite(pout, send_data, send_lenght, sent_data_lenght, send_delay)
        # logging.info("enviando datos")
        # logging.info(str(send_data.value))

        receive_data = ctypes.create_string_buffer(data_len)
        receive_length = (ctypes.c_ulong * 1)()
        ctypes.cast(receive_length, ctypes.POINTER(ctypes.c_ulong))
        receive_delay = self.read_delay
        expected_receive_length = data_len

        self.api._MPUSBRead(pin, receive_data, expected_receive_length, receive_length, receive_delay)
        self.api._MPUSBClose(pin)
        self.api._MPUSBClose(pout)

        return receive_data

    def request_fake(self, data, data_len):
        #logging.info("enviando linea: "+data.__str__())
        data = "".join(data)
        #logging.info("bytes enviados "+str(len(data)) + " '" + data + "'")
        #print data
        return chr(0x00)*data_len

    def execute(self, delay, requests):
        """ejecutar pila de instucciones del AD"""
        data = []
        for c in requests:
            if self.debug:
                response = self.request_fake(*c)
                data.append(response)
            else:
                response = self.request(*c)
                data.append(response.value)

            sleep(delay)
        return data
