#!/usr/bin/python3
# -*- coding: UTF-8 -*-

'''
    用户，用来发起交易以及接收和广播消息
    假设：只有当前一笔交易得到确认后，才能发起下一笔交易，不能连续发起交易！!
'''
import socket
import json
import threading
from wallet import Wallet
import sys
from communicate import *
from transaction import *

if len(sys.argv) != 2:
    print('Usage : %s <name>' % sys.argv[0])
    sys.exit(1)
    
myname = sys.argv[len(sys.argv)-1]
addr,private_key,public_key = get_addr_key(myname)

block_chain = get_whole_chain()
t = threading.Thread(target=update_blockchain_sender,args=(block_chain,))
t.start()  # update blockchain 

my_wallet = Wallet(public_key)

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
PORT = 1060
#network = '<broadcast>'
network = '10.255.255.255'

# runtime 
# 
while True:
    print('Please input a new transaction')
    recepient = input('recepient: ')
    amount = float(input('amount: ')) 
    new_transaction = my_wallet.handle_an_order(private_key,public_key,recepient,amount,block_chain.chain)
    print(new_transaction)
    print('=================')
    if new_transaction != None:
        s.sendto(bytes(json.dumps(new_transaction),'utf-8'), (network, PORT))
    else:
        print('invalid transaction!')
    anymore = input('have next?[y/n]\n')
    if anymore != 'y':
        break
s.close()