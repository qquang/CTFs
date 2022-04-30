#! python3
import requests
url ='http://challenge01.root-me.org/web-serveur/ch2/'
header={
    'User-Agent':'Admin'
}
r = requests.get(url,headers=header)
print(r.text)