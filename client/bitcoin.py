#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from block import Block
import random
import datetime as date

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
    
    def generate_first_block(self):
        first_block = Block(0,date.datetime.now(),[{
            'sender': 0,
            'recipient': 0,
            'amount':1
        }],0,0)
        self.chain.append(first_block)

    def add_new_block(self,proof):
        previous_block = self.get_last_block()
        block_to_add = Block(previous_block.index + 1,date.datetime.now(), self.current_transactions, previous_block.getHash(), proof)
        self.chain.append(block_to_add)
        self.current_transactions = []

    def add_new_transaction(self, transaction):
        self.current_transactions.append({
            'sender': transaction['sender'],
            'recepient': transaction['recepient'],
            'amount': transaction['amount']
        })

    def get_last_block(self):
        return self.chain[-1]
    
    def pow(self):
        target = random.randint(1,1000000)
        proof = random.randint(1,1000000)
        if target == proof:
            self.add_new_block(proof)
            return True
        else:
            return False

    def to_print(self):
        for item in self.chain:
            print("transactions : {}\nHash: {}\n".format(item.transactions, item.getHash()))

'''def main():
    block_chain = Blockchain()
    block_chain.generate_first_block()
    num = 20
    num1 = 2
    for i in range(0,num):
        for j in range(0,num1):
            block_chain.add_new_transaction(random.randint(1,100),random.randint(1,100),random.random()*100)
        block_chain.add_new_block(random.randint(1,100))
    block_chain.display()
    '''