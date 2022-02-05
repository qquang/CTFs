#!python3
import requests
import string
sess= requests.Session()
url ="http://localhost:2010/?"
HEADERS={
    "Cookie":"PHPSESSID=d63db7c5ed0f034cc8a83d69f80b704c"
}
#[43:107]
#[11:43]



## EBC attack
## sizeblock=16
## payload= 'a' * i + key_add + 'a'*i for i in range(15,-1,-1)
## so sanh block1:a*i+key+padding voi block2: a*15+padding
## trung thi ra dc ki tu key hop le
## tiep tuc bruteforce den khi nao het dc 15 bytes
filter=string.ascii_letters+string.digits
key_add=''
def check():
    req=sess.get(url+"file=/tmp/sess_d63db7c5ed0f034cc8a83d69f80b704c",headers=HEADERS).text
    a=req.index('"')+1 
    if req[a:a+32]==req[a+32:a+64]: # so sanh block1 vs block 2
        return True
for i in range(15,-1,-1):
    for key in filter:
        payload='a'*i+key_add+key+'a'*i
        req2=sess.get(url+'name='+payload,headers=HEADERS)
        if check():
            key_add+=key
            print(key_add)
            break
