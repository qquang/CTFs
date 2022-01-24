#!python3 
from hashlib import md5
from itertools import combinations_with_replacement
import string

n = '0e'

for i in range(1,25):
    d = combinations_with_replacement(string.digits,i)
    for p in d:
        hash1 = n + ''.join(p)
        m = md5()
        m.update(hash1.encode('utf-8'))
        hash2 = m.hexdigest()
        if hash2[:2] == n and hash2[2:].isnumeric():
            print(hash1)
            print(hash2)
            break