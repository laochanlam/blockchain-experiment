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
        # self.signature = 

    def display(self):
        return {
            'a_addr': self.a_addr
            'a_public_key': self.a_public_key
            'b_addr': self.b_addr
            'b_public_key': self.b_public_key
            'a_value': self.a_value
            'b_value': self.b_value
            'unspent': self.unspent_list
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

def create_transaction(a_addr,a_public_key,b_addr,b_public_key,a_value,b_value,unspent_list,a_secretkey):
    new_transaction = Transaction(a_addr,b_addr,a_value,b_value,unspent_list)
    new_transaction.get_signature(a_secretkey)
    return new_transaction

def verify_transacton(transaction,public_key):
    # check the signature with A's public_key
    # check the A's history UTXO

