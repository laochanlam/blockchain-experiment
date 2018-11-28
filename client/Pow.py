from pool import Pool
from blockchain import Blockchain
from block import Block
from transaction import Transaction
from communicate import *
import socket
import json
import hashlib 
import datetime as date

def proof_of_work(my_publickey, block_chain, tx_pool,s,soc):
    while True:
        current_transactions = []
        sum = 9
        while ((not tx_pool.isempty()) and (sum>0)): 
            current_transactions.append(tx_pool.pop())
            sum = sum - 1 
        # return nonce and current tx set
        # add myself mining
        mining_transaction = Transaction('0','0',my_publickey,my_publickey,0,50,[])
        current_transactions.append(mining_transaction)

        nonce = 0

        while True:
            previous_block = block_chain.get_last_block()
            block_to_add = Block(previous_block.index + 1,date.datetime.now(), current_transactions, previous_block.getHash(), nonce)
            nonce += 1
            context = json.dumps(block_to_add)
            hex_dig = hashlib.sha256(context).hexdigest()
            if (hex_dig[0] == '0'):
                break

        block_chain.chain.append(block_to_add)
        print(block_chain.get_last_block().display())
        # broadcast a block
        send_block(s,block_chain.get_last_block().display(),soc)