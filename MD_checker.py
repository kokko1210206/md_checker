# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 01:00:29 2021

@author: kokko
"""

import glob
import platform
import can
from serial.tools import list_ports
import serial
import time
import ctypes

    
class MD_check:
    finish = False
    
    def __init__(self,portname,_bitrate):
        self.canbus = can.interfaces.slcan.slcanBus(channel=portname,bitrate=_bitrate)
        self.serialbus = serial.Serial(portname, _bitrate)
    
    def count_devices(self,devices):
        if len(devices) == 1:
            self.serial_port = devices[0] 
            print('use ' + self.serial_port)
        elif len(devices) == 0:
            print('Serial port not found.\nPlease make sure the device is connected.\n')
            self.finish = True
        else:
            print('Multiple serial ports are connected to the device.')
            self.finish = True
            
    def search_device(self):
        OS = platform.system()
        if OS == 'Linux':
            devices = glob.glob('/dev/ttyACM?')
            self.count_devices(devices)
        elif OS == 'windows':
            _devices = list_ports.comports()
            devices = [info.device for info in _devices]
            self.count_devices(devices) 
        elif OS == 'Darwin':
            devices = glob.glob('/dev/tty.usbserial*')
            self.count_devices(devices)
    
    def can_msg(self,aid,data):
        msg = can.Message(arbitration_id = aid\
                          ,dlc = len(data)\
                          ,data = bytearray(data))
        return msg
    
    def can_ready(self):
        self.search_device()
        self.bus.send(b'\r');
        time.sleep(0.01)
        self.bus.send(b'C\r');
        time.sleep(0.01)
        self.bus.send(b'S8\r');
        time.sleep(0.01)
        self.bus.send(b'O/r')
        time.sleep(0.01)
        
    def can_send(self,canid,data):
        canmsg = self.can_msg(canid,data)
        self.bus.send(canmsg)
    
if __name__ == '__main__':
    print('MD Checker β\n\n')
    canid = 0x4e8
    MD_check.can_ready()
    time.sleep(0.2)
    MD_check.can_send(ctypes.c_uint16(canid),ctypes.c_uint(1))
    time.sleep(0.2)
    MD_check.can_send(ctypes.c_uint16(canid+1),ctypes.float32(1.0))
    time.sleep(1.0)
    MD_check.can_send(ctypes.c_uint16(canid+1),ctypes.float32(-1.0))
    time.sleep(1.0)
    MD_check.can_send(ctypes.c_uint16(canid),ctypes.c_uint(0))
    
