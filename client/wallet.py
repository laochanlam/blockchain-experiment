import transaction
class Wallet(object):
    def __init__(self,public_key):
        self.public_key = public_key
    
    def update_money(self,public_key,blockchain):
        self.tansactions_index,self.money = search_transaction(public_key,blockchain)

    def spent_money(self,a_addr,a_public_key,b_addr,b_public_key,b_value,a_secretkey):
        create_tansaction(a_addr,a_public_key,b_addr,b_public_key,self.money-b_value,b_value,self.transaction_index,a_secretkey)
