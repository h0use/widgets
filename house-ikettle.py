#!/usr/bin/env python
import time
import socket

TCP_IP = '192.168.1.107'
TCP_PORT = 2000
BUFFER_SIZE = 10
INITIATE = "HELLOKETTLE\n"
START = "set sys output 0x4\n"
TEMP = "set sys output 0x2\n" #Fill in your desired temperature, this is 95 degrees
WARM = "set sys output 0x8\n" #including this one means it will keep it warm for 30 minutes. If you want to get rid of this, also remove it below.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(INITIATE)
data = s.recv(BUFFER_SIZE)
print "Initiate", data
s.send(START)
data = s.recv(BUFFER_SIZE)
print "Start data", data
time.sleep(1)
s.send(TEMP)
data = s.recv(BUFFER_SIZE)
print "Temp", data
#If you don't want to keep your tea warm, remove until the next comment.
# time.sleep(1)
# s.send(WARM)
# data = s.recv(BUFFER_SIZE)
# print "Warm:", data
#Leave the s.close() intact :)
s.close()
