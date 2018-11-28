from sortedcontainers import SortedDict
import json

# transaction pool
class Pool(object):   
    pool = []

    def __init__(self):
        pass

    def push(self,transaction):  
        self.pool.append(transaction)
        # True stand for success
        return True
        
    def pop(self):
        # pop the transaction with largest b_value
        # add verify transaction #########################
        max_element = max(self.pool, key=lambda x:x['b_value'])
        return self.pool.pop(self.pool.index(max_element))

    def display(self):
        return json.dumps(self.pool, indent=4)

    def isempty(self):
        # if pool is empty
        if not self.pool:
            return True
        else:
            return False