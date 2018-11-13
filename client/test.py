import pool

tx0 = {
    'a_addr': 'test0',
    'a_public_key': 'test0',
    'b_addr': 'test0',
    'b_public_key': 'test0',
    'a_value': int(10), # refund
    'b_value': int(15), # to B
    'unspent': 'test0',
    'signature': 'test0'
}

tx1 = {
    'a_addr': 'test1',
    'a_public_key': 'test1',
    'b_addr': 'test1',
    'b_public_key': 'test1',
    'a_value': int(231), # refund
    'b_value': int(1), # to B
    'unspent': 'test1',
    'signature': 'test1'
}

tx2 = {
    'a_addr': 'test2',
    'a_public_key': 'test2',
    'b_addr': 'test2',
    'b_public_key': 'test2',
    'a_value': int(122), # refund
    'b_value': int(12), # to B
    'unspent': 'test2',
    'signature': 'test2'
}
