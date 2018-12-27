from transaction import *

class Wallet(object):
    def __init__(self,public_key):
        self.public_key = public_key
    
    def update_money(self,public_key,blocks):
        self.transactions_index,self.money = search_transaction(public_key,blocks)

    def spent_money(self,a_addr,a_public_key,b_addr,b_public_key,b_value,a_secretkey):
        return create_transaction(a_addr,a_public_key,b_addr,b_public_key,self.money-b_value,b_value,self.transactions_index,a_secretkey)

    def handle_an_order(self,my_private_key,my_public_key,receiver_name,amount,blocks):
        b_addr,b_private_key,b_public_key = get_addr_key(receiver_name)
        self.update_money(my_public_key,blocks)
        if (self.money >= amount):
            return self.spent_money(my_public_key,my_public_key,b_addr,b_public_key,amount,my_private_key).display()
        else:
            return None