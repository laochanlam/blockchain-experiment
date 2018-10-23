#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import socket
import json

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

PORT = 1060

#network = '<broadcast>'
network = '10.255.255.255'

while True:
    print('Please input a transaction')
    sender = input('sender: ')
    recepient = input('recepient: ')
    amount = input('amount: ')
    print('=================')
    s.sendto(bytes(json.dumps({'sender': sender,
                               'recepient': recepient,
                               'amount': amount}),'utf-8'), (network, PORT))
    anymore = input('have next?[y/n]\n')
    if anymore != 'y':
        break
s.close()
