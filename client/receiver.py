#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import socket               # 导入 socket 模块
import json
import select
from bitcoin import Blockchain
from block import Block
import threading
import transaction

def send_block(s,block,socket):
    s.sendto(bytes(json.dumps(block),'utf-8'),socket)

def send_blockchain(block_chain):
    ss = socket.socket()
    ip_port = ('',1060)
    ss.bind(ip_port)
    ss.listen(5)
    while True:
        connect,addr = ss.accept()
        data = connect.recv(1024)

        for block in block_chain.chain:
            connect.sendall(bytes(json.dumps(block.display()),'utf-8'))
            data = connect.recv(1024)
        connect.sendall(bytes('exit','utf-8'))    
        connect.close()




def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)         # 创建 socket 对象
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)

    network='10.255.255.255'

    host = socket.gethostname() # 获取主机名
    port = 1060                # 设置端口好

    s.bind(('',port))
    inputs = [s]

    block_chain = Blockchain()

    t = threading.Thread(target=send_blockchain,args=(block_chain,))
    t.start()  # send blockchain 

    ip_port=('10.0.0.1',1060)
    sk = socket.socket()
    sk.connect(ip_port)
    sk.sendall(bytes('ok','utf-8'))
    
    while True:  # get the whole blockchain
        data = sk.recv(1024)
        if data == bytes('exit','utf-8'):
             break
        print (data)
        block_json = json.loads(data.decode('utf-8'))
        block_to_add = Block(block_json['index'],block_json['timestamp'],block_json['transactions'],block_json['pre_hash'],block_json['proof'])
        block_chain.chain.append(block_to_add)
        sk.sendall(bytes('ok','utf-8'))
    sk.close()

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
                if verify_transaction(rec_transaction,rec_transaction.a_public_key):
                    block_chain.add_new_transaction(receive)
                    print(receive)
            else:   # receiver a block
                if block_chain.get_last_block().getHash() == receive['pre_hash']:
                    block_to_add = Block(receive['index'],receive['timestamp'],receive['transactions'],receive['pre_hash'],receive['proof'])
                    print ('get a broadcast block! from{}'.format(addr))
                    block_chain.chain.append(block_to_add)
            
        if block_chain.pow():
            print(block_chain.get_last_block().display())
            send_block(s,block_chain.get_last_block().display(),(network,port))

if __name__ == '__main__':
    main()
        

