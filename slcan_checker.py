# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 01:00:29 2021

@author: kokko
"""

import glob
import platform
import can
import can.interfaces.slcan
import serial
from serial.tools import list_ports
import struct
import tkinter
from tkinter import messagebox
    
class slcan_check:
    
    _device_ok = False
    
    def setting(self):
        try:
            self.canbus = can.interfaces.slcan.slcanBus(channel=self.serial_port,bitrate=1000*1000)
        except serial.SerialException:
            text='could not open port "' + self.serial_port + '" : PermissionError'
            tkinter.messagebox.showinfo('info',text)
        
    
    def count_devices(self,devices):
        if len(devices) == 1:
            self.serial_port = devices[0] 
            text='use ' + self.serial_port
            tkinter.messagebox.showinfo('info',text)
            self.setting()
            self._device_ok = True
        elif len(devices) == 0:
            text='Serial port not found.\nPlease make sure the device is connected.\n'
            tkinter.messagebox.showinfo('info',text)
            
        else:
            text='Multiple serial ports are connected to the device.'
            tkinter.messagebox.showinfo('info',text)
            
            
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

    def can_send_done(self,event):
        global int_bool
        global float_bool
        global id_entry
        global value_entry
        self.search_device()
        text = ""
        if (self._device_ok == False):{}
        elif (int_bool.get() == True and float_bool.get() == True) or (int_bool.get() == False and float_bool.get() == False):
            text = "Please select one type."
            tkinter.messagebox.showinfo('info',text)
        elif int_bool.get() == True:
            value = [value_entry.get()]
            self.can_send(id_entry.get(),data=value)
        elif float_bool.get() == True:
            value = [value_entry.get()]
            self.can_send(id_entry.get(),data=struct.pack('>f', *value))
    
    def port_check(self,event):
        self.search_device()
        
        
        

    
if __name__ == '__main__':
    gui = tkinter.Tk()
    gui.title(u"slcan Checker v2.0")
    gui.geometry("300x75")
    checker = slcan_check()
    
    canid_label = tkinter.Label(text=u'ID : ')
    canid_label.place(x=9,y=5)

    type_label = tkinter.Label(text=u'type')
    type_label.place(x=145,y=1)

    id_entry = tkinter.Entry(width=15)
    id_entry.insert(tkinter.END,"Please entry id")
    id_entry.place(x=33,y=5)

    int_bool = tkinter.BooleanVar()
    float_bool = tkinter.BooleanVar()
   
    CheckBox1 = tkinter.Checkbutton(text=u"uint", variable=int_bool)
    CheckBox1.place(x=185,y=1)

    CheckBox2 = tkinter.Checkbutton(text=u"float", variable=float_bool)
    CheckBox2.place(x=185,y=23)

    canid_label = tkinter.Label(text=u'value : ')
    canid_label.place(x=145,y=48)
    
    value_entry = tkinter.Entry(width=18)
    value_entry.insert(tkinter.END,"Please entry value")
    value_entry.place(x=185,y=48)


    button1 = tkinter.Button(gui, text=u'send',width=9)
    button1.bind("<Button-1>",checker.can_send_done)
    button1.place(x=40,y=35)
    
    
    
    gui.mainloop()
    
