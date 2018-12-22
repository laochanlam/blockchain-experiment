from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
from block import Block
import hashlib 
import json
import base64

class Transaction(object):
    def __init__(self,a_addr,a_public_key,b_addr,b_public_key,a_value,b_value,unspent_list):
        self.a_addr = a_addr
        self.a_public_key = a_public_key
        self.b_addr = b_addr
        self.b_public_key = b_public_key
        self.a_value = a_value
        self.b_value = b_value
        self.unspent = unspent_list
    
    def get_signature(self,secret_key):
        # add digital signature
        message = self.a_addr + self.a_public_key + self.b_addr + \
                  self.b_public_key + str(self.a_value) + str(self.b_value)
        for i, val in enumerate(self.unspent):
             message = message + str(val[0]) + str(val[1])
        rsakey = RSA.importKey(secret_key.encode())
        signer = Signature_pkcs1_v1_5.new(rsakey)
        digest = SHA.new()
        digest.update(message.encode())
        sign = signer.sign(digest)
        signature = base64.b64encode(sign) 
        self.signature = signature.decode()
       

    def display(self):
        return {
            'a_addr': self.a_addr,
            'a_public_key': self.a_public_key,
            'b_addr': self.b_addr,
            'b_public_key': self.b_public_key,
            'a_value': self.a_value,
            'b_value': self.b_value,
            'unspent': self.unspent,
            'signature': self.signature
        }
    @staticmethod
    def rebuild(transaction_json):
        a_addr = transaction_json['a_addr']
        a_public_key = transaction_json['a_public_key']
        b_addr = transaction_json['b_addr']
        b_public_key = transaction_json['b_public_key']
        a_value = transaction_json['a_value']
        b_value = transaction_json['b_value']
        unspent = transaction_json['unspent']
        new_transaction = Transaction(a_addr,a_public_key,b_addr,b_public_key,a_value,b_value,unspent)
        new_transaction.signature = transaction_json['signature']
        return new_transaction

def search_transaction(public_key,blockchain):
    # get all UTXO from blockchain with public_key
    # return a list of all UTXO's index and total value
    # 寻找某个公钥拥有的UTXO，返回所有这些UTXO的索引（块号+块中交易号）和总价值
    # return (index,value)  
    # need a new algorithm ################################ 
    
    unspent_list_of_public_key = []
    value = 0
    end = 0
    length = len(blockchain)

    for i in range(length):
        for j in range(len(blockchain[-i - 1].transactions)):
            if blockchain[-i - 1].transactions[-j - 1]['b_public_key'] == public_key:
                unspent_list_of_public_key.append((length - i - 1,len(blockchain[-i - 1].transactions) - j - 1))
                value += blockchain[-i - 1].transactions[-j - 1]['b_value']
            elif blockchain[-i - 1].transactions[-j - 1]['a_public_key'] == public_key:
                unspent_list_of_public_key.append((length - i - 1,len(blockchain[-i - 1].transactions) - j - 1))
                if len(blockchain[-i - 1].transactions[-j - 1]['unspent']) > 0:
                    end = max(end , blockchain[-i - 1].transactions[-j - 1]['unspent'][-1][0] + 1)
                value += blockchain[-i - 1].transactions[-j - 1]['a_value']
        if length - i - 1 == end :
            break
    return (unspent_list_of_public_key, value)

def create_transaction(a_addr,a_public_key,b_addr,b_public_key,a_value,b_value,unspent_list,a_secretkey):
    new_transaction = Transaction(a_addr,a_public_key,b_addr,b_public_key,a_value,b_value,unspent_list)
    new_transaction.get_signature(a_secretkey)
    return new_transaction

def verify_transaction(blocks,transaction,public_key):
    # check the signature with A's public_key
    # check the A's history UTXO
    # verify existed transaction and its unspent list ###################### 
    '''
    收到一个交易，验证该交易的数字签名是否与发出者的公钥相匹配，若匹配，进一步验证发送者的交易是否合法
    '''
    message = transaction['a_addr'] + transaction['a_public_key'] + transaction['b_addr'] + \
                  transaction['b_public_key'] + str(transaction['a_value']) + str(transaction['b_value'])
    total_utxo = 0
    unspent,value = search_transaction(public_key,blocks)
    for i, val in enumerate(transaction['unspent']) :
        val = tuple(val)
        if unspent.count(val) == 0: 
            return False
        message = message + str(val[0]) + str(val[1])
        apk = blocks[val[0]].transactions[val[1]]['a_public_key']
        avalue = blocks[val[0]].transactions[val[1]]['a_value']
        bpk = blocks[val[0]].transactions[val[1]]['b_public_key']
        bvalue = blocks[val[0]].transactions[val[1]]['b_value']
        if apk == transaction['a_public_key'] :
            total_utxo = total_utxo + avalue
        if bpk == transaction['a_public_key'] :
            total_utxo = total_utxo + bvalue
    
    rsakey = RSA.importKey(public_key.encode())
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new()
    # Assumes the data is base64 encoded to begin with
    digest.update(message.encode())
    is_verify = verifier.verify(digest, base64.b64decode(transaction['signature']))
    
    return is_verify and total_utxo == transaction['a_value'] + transaction['b_value']

def check_block(blocks, block):
    # 验证block的hash值以及每一笔交易是否合法，返回true/false
    # verify hash code
    context = json.dumps(block.display())
    hex_dig = hashlib.sha256(context.encode()).hexdigest()

    if hex_dig[0:4] != '0'*4:   
        return False

    # verify repeated transactions in one block
    for i in range(len(block.transactions)):
        for j in range(i):
            if (block.transactions[i]['a_public_key'] == block.transactions[j]['a_public_key']):
                return False
    # verify transaction
    for i, val in enumerate(block.transactions):
        if (not (i == len(block.transactions) -1)) and (not verify_transaction(blocks, val, val['a_public_key'])) :
            return False
    return True

def generate_account(name):
    random_generator = Random.new().read
    rsa = RSA.generate(1024,random_generator)
    private_pem = rsa.exportKey()
    with open('../userKey/' + name + '-private.pem','w') as f:
        f.write(private_pem.decode())
    public_pem = rsa.publickey().exportKey()
    with open('../userKey/' + name + '-public.pem','w') as f:
	    f.write(public_pem.decode())

def get_addr_key(name):
    '''
    得到本机地址以及公钥
    return (addr, public_key) is modified into
    return (addr, private_key, public_key)
    assuming addr is the same as public_key
    '''
    try:
        with open('../userKey/' + name + '-private.pem') as fpr:
            prkey = fpr.read()
        with open('../userKey/' + name + '-public.pem') as fpu:
            pukey = fpu.read()
    except:
        generate_account(name)
        with open('../userKey/' + name + '-private.pem') as fpr:
            prkey = fpr.read()
        with open('../userKey/' + name + '-public.pem') as fpu:
            pukey = fpu.read()
    return (pukey, prkey, pukey)
