import socket   # 导入 socket 模块
import select            
import json
import threading
from blockchain import Blockchain
from block import Block
from transaction import *
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64

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
####################
    t = threading.Thread(target=wait_consens, args=(block_pool, f, block_chain, 'user'))
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
                        #(block, the number of true in checking, the number of false in checking, the number of true in consens, the number of false in consens)
                        block_pool.append((block_to_add,0,0,0,0))

# developing #######################
def signing_commit(block, commit, secret_key):
    # block
    # commit: True or False
    # public_key
    # commit message in port 1061
    # calculate a dict object "sign"
    msg = {
        'bh': block.getHash(),
        'cm': True
    }
    plain_msg = msg['bh']
    print(msg['bh'])
    rsakey = RSA.importKey(secret_key.encode())
    signer = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new(plain_msg.encode())
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    sign = {
         'message': msg,
         'signature': signature.decode()
    }
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    PORT = 1061
    #network = '<broadcast>'
    network = '10.255.255.255'
    soc = (network, PORT)
    send_message(s,sign,soc)


def wait_checking(block_pool, f, secret_key):
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
            blockhash = receive['message']['bh']
            commit = receive['message']['cm']
            rec_sign = receive['signature']
            message = receive['message']['bh']
            is_verify = False
            verifier = []
            # verify the signature
            with open('../pbft/members-public.pem') as pbft:
                members = pbft.read().split('\\\n')
            for i, val in enumerate(members):
                rsakey = RSA.importKey(val.encode())
                verifier.append(Signature_pkcs1_v1_5.new(rsakey))
            # Assumes the data is base64 encoded to begin with
            digest = SHA.new(message.encode())
            for i, val in enumerate(members):
                is_verify = verifier[i].verify(digest, base64.b64decode(receive['signature']))
                if (is_verify):
                    break
            #is_verify == true
            if(is_verify):
                #To find the block
                for i, val in enumerate(block_pool):
                    if(val[0].getHash() == blockhash):
                        if(commit):
                            val = (val[0],val[1]+1,val[2],val[3],val[4])
                        else:
                            val = (val[0],val[1],val[2]+1,val[3],val[4])
                        block_pool[i] = val
                        if(val[1] + val[2] > 3 * f):
                            if (val[1] > val[2]):
                               commit = True
                            else:
                               commit = False
                            msg = {
                               'bh':blockhash,
                               'cm':commit
                            }
                            rsakey = RSA.importKey(secret_key.encode())
                            signer = Signature_pkcs1_v1_5.new(rsakey)
                            sign = signer.sign(digest)
                            signature = base64.b64encode(sign)
                            consens_msg = {
                                'message': msg,
                                'signature': signature.decode()
                            }
                            send_message(s,consens_msg,soc)
            
def wait_consens(block_pool, f, blockchain, mode):
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
            blockhash = receive['message']['bh']
            commit = receive['message']['cm']
            rec_sign = receive['signature']
            message = receive['message']['bh']
            is_verify = False
            # verify the signature
            verifier = []
            with open('../pbft/members-public.pem') as pbft:
                members = pbft.read().split('\\\n')
            for i, val in enumerate(members):
                rsakey = RSA.importKey(val.encode())
                verifier.append(Signature_pkcs1_v1_5.new(rsakey))
            # Assumes the data is base64 encoded to begin with
            digest = SHA.new(message.encode())
            for i, val in enumerate(members):
                is_verify = verifier[i].verify(digest, base64.b64decode(receive['signature']))
                if (is_verify):
                    break
            #is_verify == true
            if(is_verify):
                #To find the block
                for i, val in enumerate(block_pool):
                    if(val[0].getHash() == blockhash):
                        if(commit):
                            val = (val[0],val[1],val[2],val[3]+1,val[4])
                        else :
                            val = (val[0],val[1],val[2],val[3],val[4]+1)
                        block_pool[i] = val
                        if(val[3] + val[4] > 3 * f):
                            if(val[3] > val[4]):
                                blockchain.chain.append(val[0])
                                if mode == 'miner':
                                    print(json.dumps(val[0].display(),indent=4))
                                    print('consensus accept a block!')
                                    print('the length of the block chain is {}'.format(len(blockchain.chain)))
                            else:
                                if mode == 'miner':
                                    print('consensus reject a block!')
                            block_pool.pop(i)
