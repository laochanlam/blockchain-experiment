import socket   # 导入 socket 模块
import select            
import json
import threading
from blockchain import Blockchain
from block import Block
from transaction import *

def send_message(s,msg,socket):
    s.sendto(bytes(json.dumps(msg),'utf-8'),socket)

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

def get_whole_chain():
    ip_port=('10.0.0.1',1060)
    sk = socket.socket()
    sk.connect(ip_port)
    sk.sendall(bytes('ok','utf-8'))
    block_chain = Blockchain()

    while True:  # get the whole blockchain
        data = sk.recv(65536)
        if data == bytes('exit','utf-8'):
             break
        print (data)
        block_json = json.loads(data.decode('utf-8'))
        block_to_add = Block(block_json['index'],block_json['timestamp'],block_json['transactions'],block_json['pre_hash'],block_json['nonce'])
        block_chain.chain.append(block_to_add)
        sk.sendall(bytes('ok','utf-8'))
    sk.close()
    return block_chain

def update_blockchain_sender(block_chain,f):
    block_pool = []
    f = 2
####################
    t = threading.Thread(target=wait_consens args=(block_pool, f, block_chain))
    t.start() 

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)         # 创建 socket 对象
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    port = 1060               # 设置端口好 
    s.bind(('',port))
    inputs = [s]
    # runtime
    while True:
        rs,ws,es = select.select(inputs,[],[],0.0) #set timeout 1s
        if rs != []:
            data, addr = s.recvfrom(65536)
            receive = json.loads(data.decode('utf-8'))
            try:
                receive['index']
            except:
                # receive a transaction
                continue
            else:
                # receiver a block
                if block_chain.get_last_block().getHash() == receive['pre_hash']:
                    block_to_add = Block(receive['index'],receive['timestamp'],receive['transactions'],receive['pre_hash'],receive['nonce'])
                    # print ('get a broadcast block! from{}'.format(addr))
                    if check_block(block_chain.chain,block_to_add):
                        #block_chain.chain.append(block_to_add)
                        block_pool.append(block_to_add)

# developing #######################
def signing_commit(block, commit, public_key):
    # block
    # commit: True or False
    # public_key
    # commit message in port 1061
    # calculate a dict object "sign"

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    PORT = 1061
    #network = '<broadcast>'
    network = '10.255.255.255'
    soc = (network, PORT)
    send_message(s,sign,soc)

def wait_checking(block_pool, f):
    # wait 2f+1 check info then broadcast a consens info
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    PORT = 1062  # consensus message in port 1062
    #network = '<broadcast>'
    network = '10.255.255.255'
    soc = (network, PORT)

    rec_s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)         # 创建 socket 对象
    rec_s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    port = 1061               # 设置端口好 
    rec_s.bind(('',port))
    inputs = [rec_s]
    while True:
        rs,ws,es = select.select(inputs,[],[],0.0) #set timeout 1s
        if rs != []:
            # get a message in port 1061
            data, addr = rec_s.recvfrom(65536)
            receive = json.loads(data.decode('utf-8'))
            # handle the checking message ##############
            # create a consensus messaage "consens_msg"
            send_message(s,consens_msg,soc)

def wait_consens(block_pool, f, blockchain):
    # wait 2f+1 consens info then insert block
    rec_s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)         # 创建 socket 对象
    rec_s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    port = 1062             # 设置端口好 
    rec_s.bind(('',port))
    inputs = [rec_s]
    while True:
        rs,ws,es = select.select(inputs,[],[],0.0) #set timeout 1s
        if rs != []:
            # get a message in port 1061
            data, addr = rec_s.recvfrom(65536)
            receive = json.loads(data.decode('utf-8'))
            # handle the consensus message ##############
            # blockchain.chain.append()
