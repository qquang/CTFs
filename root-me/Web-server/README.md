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



