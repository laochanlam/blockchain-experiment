#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import socket               # 导入 socket 模块
import json
import select
from bitcoin import Blockchain
from block import Block



def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)         # 创建 socket 对象
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)


    host = socket.gethostname() # 获取主机名
    port = 1060                # 设置端口好

    s.bind(('',port))
    inputs = [s]

    block_chain = Blockchain()
    block_chain.generate_first_block()
    while True:
        rs,ws,es = select.select(inputs,[],[],0.0) #set timeout 1s
        if rs != []:
            data, addr = s.recvfrom(65536)
            transaction = json.loads(data.decode('utf-8'))
            print(transaction)
            block_chain.add_new_transaction(transaction)
        if block_chain.pow():
            print(block_chain.get_last_block().display())

if __name__ == '__main__':
    main()
        

