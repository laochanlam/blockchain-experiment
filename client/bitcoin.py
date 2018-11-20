#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from block import Block
from transaction import Transaction
from pool import Pool
import random
import datetime as date

class Blockchain(object):
    def __init__(self):
        self.chain = [] # use array
        self.transaction_pool = Pool()
    b
    def generate_first_block(self):
        first_block = Block(0,date.datetime.now(),[{
            'a_addr': '0'
            'a_public_key': '0'
            'b_addr': '10.0.0.1'
            'b_public_key': '10.0.0.1'
            'a_value': 0
            'b_value': 1
            'unspent': []
            'signature': '0'
        }],0,0)
        self.chain.append(first_block)

    def add_new_block(self,proof,self_mining):
        previous_block = self.get_last_block()
        # use transaction pool to pop 15 tansactions
        current_transactions = []
        sum = 9
        while ((not self.transaction_pool.isempty()) and (sum>0)): 
            current_transactions.append(self.transaction_pool.pop())
            sum = sum - 1 
        # current_transactions.append() mining

        block_to_add = Block(previous_block.index + 1,date.datetime.now(), current_transactions, previous_block.getHash(), proof)
        self.chain.append(block_to_add)
            
    def add_new_transaction(self, transaction):
        self.transaction_pool.push(transaction)

    def get_last_block(self):
        return self.chain[-1]
    

    def pow(self,public_key):
    '''
        取交易池pool中前9个交易+1个给自己50个bitcoin的交易（挖矿）
        计算pow，若成功返回true并创建新块: self.add_new_block(proof,self_mining)
        否则返回false
    '''

    def to_print(self):
        for item in self.chain:
            print("transactions : {}\nHash: {}\n".format(item.transactions, item.getHash()))

