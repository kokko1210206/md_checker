# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 01:00:29 2021

@author: kokko
"""

import glob
import platform
import can
import can.interfaces.slcan
from serial.tools import list_ports
import time
import os
import stat
import struct
    
class MD_check:
    finish = False
    
    def setting(self):
        self.canbus = can.interfaces.slcan.slcanBus(channel=self.serial_port,bitrate=1000*1000)
    
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
        elif OS == 'Windows':
            _devices = list_ports.comports()
            devices = [info.device for info in _devices]
            self.count_devices(devices) 
        elif OS == 'Darwin':
            devices = glob.glob('/dev/tty.usbserial*')
            self.count_devices(devices)
    
    def can_msg(self,aid,data):
        msg = can.Message(arbitration_id = aid\
                          ,dlc = len(data)\
                          ,is_extended_id=False
                          ,data = bytearray(data))
        return msg
    
        
    def can_send(self,canid,data):
        canmsg = self.can_msg(canid,data)
        self.canbus.send(canmsg)
    
if __name__ == '__main__':
    print('MD Checker β\n\n')
    canid = 0x4e8
    checker = MD_check()
    checker.search_device()
    checker.setting()
    time.sleep(1.2)
    checker.can_send(canid,data=[0x01])
    time.sleep(1.2)
    data=[1.0]
    checker.can_send(canid+1,data=struct.pack('>f', *data))
    time.sleep(1.5)
    data=[-1.0]
    checker.can_send(canid+1,data=struct.pack('>f', *data))
    time.sleep(1.5)
    checker.can_send(canid,data=[0x00])
    
