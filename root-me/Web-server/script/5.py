#!python3
from itsdangerous import base64_encode
import requests
import base64
with open('./user.txt') as f1:
    list1 = [i.rstrip('\n') for i in f1]
with open('./password.txt') as f2:
    list2 = [i.rstrip('\n') for i in f2]
output = open('payload.txt','w')
for i in range(len(list1)):
    str1=''
    for j in range(len(list2)):
        str1=(list1[i]+':'+list2[j]).encode("ascii")
        output.write(base64.b64encode(str1).decode()+'\n')

