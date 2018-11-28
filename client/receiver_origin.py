#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import socket               # 导入 socket 模块
import json
import select
from blockchain import Blockchain
from block import Block
from pool import Pool
import threading
from transaction import *
from communicate import *
from Pow import *
import datetime as date
import hashlib 
import sys
  
def send_block(s,block,socket):
    s.sendto(bytes(json.dumps(block),'utf-8'),socket)

def send_blockchain(block_chain):
    ss = socket.socket()
    ip_port = ('',1060)
    ss.bind(ip_port)
    ss.listen(5)
    while True:
        #print ('end')
        connect,addr = ss.accept()
        #print ('on')
        data = connect.recv(1024)
        #print ('on1')
        for block in block_chain.chain:
            connect.sendall(bytes(json.dumps(block.display()),'utf-8'))
            data = connect.recv(1024)
        connect.sendall(bytes('exit','utf-8'))    
        connect.close()

def main(): 
    # get addr and publickey
    myname = sys.argv[0]
    addr,private_key,public_key = get_addr_key()

    tx_pool = Pool()
    block_chain = Blockchain()

    t1 = threading.Thread(target=send_blockchain,args=(block_chain,))
    t1.start()

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)         # 创建 socket 对象
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    network='10.255.255.255'
    port = 1060                # 设置端口好
    s.bind(('',port))
    inputs = [s]

    # POW
    t2 = threading.Thread(target=proof_of_work,args=(public_key, block_chain, tx_pool,s,(network,port),))
    t2.start()  

    # runtime
    while True:
        rs,ws,es = select.select(inputs,[],[],0.0) #set timeout 1s
        if rs != []:
            data, addr = s.recvfrom(65536)
            receive = json.loads(data.decode('utf-8'))
            try:
                receive['index']
            except:  # receive a transaction
                rec_transaction = rebuild(receive)
                if verify_transaction(block_chain.chain,rec_transaction,rec_transaction.a_public_key):
                    #block_chain.add_new_transaction(receive)
                    tx_pool.push(receive)
                    print(receive)
            else:   # receiver a block
                if len(block_chain.chain) == 0:
                    has = 0
                else
                    has = block_chain.get_last_block().getHash()
                if has == receive['pre_hash']:
                    block_to_add = Block(receive['index'],receive['timestamp'],receive['transactions'],receive['pre_hash'],receive['proof'])
                    print ('get a broadcast block! from{}'.format(addr))
                    if check_block(block_chain.chain,block_to_add)
                        block_chain.chain.append(block_to_add)



if __name__ == '__main__':
    main()
        