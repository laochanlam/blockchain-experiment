#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import datetime as date
import hashlib as hasher

class Block(object):
    def __init__(self, index, timestamp, transactions, previous_hash, nonce):
        self.index = index
        self.timestamp = str(timestamp)
        self.transactions = transactions
        self.pre_hash = previous_hash
        self.nonce = nonce

    def getHash(self):
        sha = hasher.sha256()
        sha.update(
            bytes(str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.pre_hash) + str(self.nonce),'utf-8')
        )
        return sha.hexdigest()

    def display(self):
        return ({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'pre_hash': self.pre_hash,
            'nonce': self.nonce
        })
