#!python3

import requests

url = 'http://challenge01.root-me.org/web-serveur/ch68/'
header={
    'X-Forwarded-For':'192.168.1.11'
}
r = requests.get(url,headers=header)

print(r.text)