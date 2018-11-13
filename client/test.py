from pool import Pool

tx0 = {
    'a_addr': 'test0',
    'a_public_key': 'test0',
    'b_addr': 'test0',
    'b_public_key': 'test0',
    'a_value': int(10), # refund to A
    'b_value': int(15), # to B
    'unspent': 'test0',
    'signature': 'test0'
}

tx1 = {
    'a_addr': 'test1',
    'a_public_key': 'test1',
    'b_addr': 'test1',
    'b_public_key': 'test1',
    'a_value': int(231), # refund to A
    'b_value': int(1), # to B
    'unspent': 'test1',
    'signature': 'test1'
}

tx2 = {
    'a_addr': 'test2',
    'a_public_key': 'test2',
    'b_addr': 'test2',
    'b_public_key': 'test2',
    'a_value': int(122), # refund to A
    'b_value': int(12), # to B
    'unspent': 'test2',
    'signature': 'test2'
}

tx_pool = Pool()

tx_pool.push(tx0)
tx_pool.push(tx1)
tx_pool.push(tx2)

print(tx_pool.pop())

print(tx_pool.display())