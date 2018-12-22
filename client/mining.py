from pool import Pool
from blockchain import Blockchain
from block import Block
from transaction import Transaction
from communicate import *
import socket
import json
import hashlib 
import datetime as date
import base64

def handle_overlay(transactions):
    now_transactions = []
    # avoid double spend
    for i in range(len(transactions)):
        flag = True
        for j in range(i):
            if (transactions[i]['a_public_key'] == transactions[j]['a_public_key']):
                flag = False
        if flag:
            now_transactions.append(transactions[i])
    return now_transactions

# handle transaction overtime caused by block updating
def update_transactions(blocks,transactions):
    now_transactions = []
    for i in range(len(transactions)):
        if i == len(transactions) - 1 or verify_transaction(blocks,transactions[i],transactions[i]['a_public_key']):
            now_transactions.append(transactions[i])
        else:
            print('transaction overtime!')
    return now_transactions

def proof_of_work(my_publickey, block_chain, tx_pool, s, soc, work_factor=0):
    while True:
        current_transactions = []
        # return nonce and current tx set
        # add myself mining 

        mining_transaction = {
            'a_addr': '0',
            'a_public_key': '0',
            'b_addr': my_publickey,
            'b_public_key': my_publickey,
            'a_value': 0.0,
            'b_value': 50.0,
            'unspent': [],
            'signature': '0'
        }

        current_transactions.append(mining_transaction)
        nonce = 0
        
        pre_previous_block = None
        print('doing PoW...')
        while True:
            if (nonce % 3 == work_factor):  
                # print(nonce)
                while ((not tx_pool.isempty()) and (len(current_transactions)<4)): 
                    add = tx_pool.pop(block_chain.chain)
                    if (add != None):
                        current_transactions.insert(0,add)
                        current_transactions = handle_overlay(current_transactions)
                if len(block_chain.chain) != 0:
                    previous_block = block_chain.get_last_block()
                    # handle transaction overtime caused by block updating
                    if pre_previous_block != None and previous_block != pre_previous_block:
                        current_transactions = update_transactions(block_chain.chain,current_transactions)
                    pre_previous_block = previous_block
                    block_to_add = Block(previous_block.index + 1,date.datetime.now(), current_transactions, previous_block.getHash(), nonce)
                else:
                    block_to_add = Block(0,date.datetime.now(), current_transactions, 0, nonce)
                context = json.dumps(block_to_add.display())
                hex_dig = hashlib.sha256(context.encode()).hexdigest()
            else:
                nonce += 1 
                continue
            nonce += 1
            if (hex_dig[0:4] == '0'*4):
                break

        if check_block(block_chain.chain,block_to_add):
            block_chain.chain.append(block_to_add)
            print('###############new block is generated######################')
            # print(json.dumps(block_chain.get_last_block().display(), indent=4))   
            # print('info ignored')
            # print('###########################################################')
            # broadcast a block
            send_block(s,block_chain.get_last_block().display(),soc)
        else:
            print('block overtime!')
