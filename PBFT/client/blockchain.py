#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from block import Block
# from transaction import Transaction
from pool import Pool
import random
import datetime as date

class Blockchain(object):
    def __init__(self):
        self.chain = [] # use array

    def get_last_block(self):
        return self.chain[-1]   

    def to_print(self):
        for item in self.chain:
            print("transactions : {}\nHash: {}\n".format(item.transactions, item.getHash()))

