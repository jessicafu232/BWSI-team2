# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 18:23:28 2022

@author: Ellie
"""
import socket

PORT = 21210

class Message:
    def __init__(self, name:str, dtype:str, data):
        '''
        name: the name of the parameter from the api documentation
        dtype: what type of data is it (uint or int and how many bits)
        data: the number we intend to transmit to the emulator
        '''
        self.name = name
        self.dtype = dtype
        
        bits_num = ''
        for i in dtype:
            if i.isdigit():
                bits_num+=i
        self.bytesnum = int(int(bits_num) / 8)
        self.data = data
    
    def convert_to_bytes(self):
        try:
            return int.to_bytes(self.data, self.bytesnum, 'big')
        except:
            return int.to_bytes(self.data, self.bytesnum, 'big', signed=True)

class Messages(Message):
    def __init__(self, messages:list):
        self.messages = messages
        self.bytesToSend = self.get_messages()
    
    def get_messages(self):
        b = bytearray()
        for msg in self.messages:
            b += bytearray(msg.convert_to_bytes())
        return b
    
    def total_bytes(self):
        total_bytes = 0
        for msg in self.messages:
            total_bytes += msg.bytesnum
        return total_bytes

DATA = Messages([
    Message('Settings Header', 'UINT16', 0xfffe),
    Message('uint16', 'UINT16', 19),
    Message('uint8', 'UINT8', 14),
    Message('uint16', 'UINT16', 29),
    Message('uint32', 'UINT32', 2022),
    Message('int8', 'INT8', 3),
    Message('int16', 'INT16', -17),
    Message('int32', 'INT32', 420)])

#stores the messages & data that will be transmitted

serverAddressPort   = ('localhost', PORT)
bufferSize = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

print("HOST SENDING", DATA.bytesToSend)

# Send to server using created UDP socket
UDPClientSocket.sendto(DATA.bytesToSend, serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)
