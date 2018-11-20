#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import socket               # 导入 socket 模块
import json
import select
from blockchain import Blockchain
from block import Block
from pool import Pool
import threading
import transaction
import datetime as date
import hashlib 

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


def pow(block_chain, tx_pool):
    current_transactions = []
    sum = 9
    while ((not tx_pool.isempty()) and (sum>0)): 
        current_transactions.append(tx_pool.pop())
        sum = sum - 1 
    # return nonce and current tx set

    previous_block = block_chain.get_last_block()
    nonce = 0

    while True:
        block_to_add = Block(previous_block.index + 1,date.datetime.now(), current_transactions, previous_block.getHash(), nonce)
        nonce += 1
        context = json.dumps(new_block)
        hex_dig = hashlib.sha256(context).hexdigest()
        if (hex_dig[0] == '0'):
            break


    return block_to_add


def main():
    # get addr and publickey
    addr,public_key = get_addr_key()

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)         # 创建 socket 对象
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)

    network='10.255.255.255'

    host = socket.gethostname() # 获取主机名
    port = 1060                # 设置端口好

    s.bind(('',port))
    inputs = [s]

    block_chain = Blockchain()
    tx_pool = Pool()


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
                    # block_chain.add_new_transaction(receive)
                    tx_pool.push(receive)
                    print(receive)
            else:   # receiver a block
                if block_chain.get_last_block().getHash() == receive['pre_hash']:
                    block_to_add = Block(receive['index'],receive['timestamp'],receive['transactions'],receive['pre_hash'],receive['proof'])
                    print ('get a broadcast block! from{}'.format(addr))
                    if check_block(block_to_add):
                        block_chain.chain.append(block_to_add)

        # POW
        block_to_add = pow(block_chain, tx_pool)
        block_chain.chain.append(block_to_add)

        print(block_chain.get_last_block().display())
        # broadcast a block
        send_block(s,block_chain.get_last_block().display(),(network,port))

if __name__ == '__main__':
    main()
        