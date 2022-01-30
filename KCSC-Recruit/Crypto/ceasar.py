#!python3
from math import gcd
from pydoc import plain
import string
import random
table = string.ascii_letters+string.digits+string.punctuation
len_table = len(table)

key=1000
plaintext='ZR7RlRptHpGjEGDJCsjDuj$DJn'
for key in range(15012022):
    ciphertext=''
    for i in range(len(plaintext)):
        number=table.index(plaintext[i])
        number= (number-key)%94 
        ciphertext+=table[number]
    if 'KCSC{' in ciphertext:
        print(ciphertext)
        break
        