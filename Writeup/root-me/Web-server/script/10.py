#!python3
import requests
url ='http://challenge01.root-me.org/web-serveur/ch32/'
r=requests.get(url,allow_redirects=False)
print(r.text)
