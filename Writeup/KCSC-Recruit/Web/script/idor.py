#!python3

import requests
url = 'http://45.77.39.59:8030/guess?number='
for i in range(100000):
   r=requests.get(url+str(i))
   if 'KCSC{' in r.text:
       print(r.text)
       break 
    