#!python3
import string
import re
import os
a='''
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAyiytHt1AKzYLwZPm1dd9uT7LgsqVj0eSLpheNd0H4xyiZCYG
ZtRYnNtGNnq7A/ubyFalExm61QNewfy71h6xhM/'''
b='''IEIoNT0VfMOIzcq0Jmoh+v6k
6/x/3GRkk/vLVolsLbkOKd4aorPMwEsZX4vMd+Sga5Mz0tx5xLFZsbl0r1vvtBl7
CtC/ojWX4+/RSGuaUVVayrU32kyCjJo3hniSaY2EvSXXHdE6nOKkF725LVrnOOIz
1/n9CYrYPV6ESEBdwS7VOen8uPwh5cFGHOV49ofmvVZNvcV2qoKFjY5UXf8fDzZ+
jBzWiCukE+3WFwgEYaBGg/a6HomkobpDqxkrYwIDAQABAoIBABht45FaLLnL8wm2
BGuMeV2b791i+0Vv4YMN2Dxr89sGh7zQN2/PctGpUUed9uEZUw6XIaU4M7IvkRCh
qFTMKqkgrVd4hwE/20vTGMG9H52Qr4Bzqpv1S8Hmw5x6DWzseAziUorOkqtcTH5j
1LIN42wNTTESfW2aRIB26Z6nCSlzHD8jpBYlrBFNsXydApEtA86PPtgs8MUsABFa
Rhy6VG9rNfzaBeRDX1m1lX+yNkqPb3xgABeYgURYgUneiTY/S5GrFfrtRAnLWVm4
audCUkxvF8OV0vJnazcMUopleBonMH2FCl3vKAjTX2xq9X24PeNXDg6SfiEEuI/g
EDtJO1ECgYEAzwBWVwbx/lvc5PP3oYXRr9IpflZ3Z9xSyopY0KpOakAXn6717x6i
s/1DwGvpmFBqUd25vhcn9ztj18GtMCtZ4dNvvyGpPwvM41Z1RVHY5REfC7sgBp8W
0N+IVR2QlyU3pjoS5t19O3g48fhOp8o3wsZ+05RpLtUhNXe0yHxk7fsCgYEA+gfZ
aCr+dgzHfdBOEwwozaRpJANchnGeILSgZZEeYmyE0RuBcatpwxKs+jG82mWYnosN
KR5CZZiPn/laySUQEB5H6Cg/OQDVyj5r49adc2H8hTCluaXtiVyxA3JqV8Ixc9TM
cRWJZdokaDbkyNXCuUuTMinzWjrNBKBZ+zg5w7kCgYBQkjwJEb39mHoJb+CSMUkl
23KlJzjA52QeS+04AyIUfy/yyqIVWeJQlqLZcedxjtNjXB9hGxhGRgqdv1gO6MDK
gob7aTm8PXaZglyRB8OZnals4oAbs66ozGj/YEuYWTco72/OBqYpEKlxnYnYC4Da
wnI5Hoo2XWTYr+hhJPIQIwKBgAxMxo0xUENObaHq1WxqdLdpFyMGZ07V2AmT2TAl
63C8FeyThdKptBI8oPXN7JRx2wgxnvwe2PVWg/pCsgyjHh8s3iy1jianu9yvJW+X
5zb94wZKVlzDpOPVA4A/6KtYikZAea42eQPhr1jRGoAmw+WJqjwVhDs0GVHY8ZRC
N9VBAoGBAJTZwrY+tZkNzURk9JLWzrevfD6BpYrQ0jchaGtzdgjdOpHo3++cdUag
9oQ8ZNKaUVDm3lyzUhO41Hw7xMmmW8JwsVvKdrRL+ZG12Ts/uiy1P0DY+HsNMr9d
xqG9YAHVmm4iJzcHeMdzLwmzR6D/x6+k2cFWwox6PxvA7ikJQEYr
-----END RSA PRIVATE KEY-----
'''

alphabets= string.ascii_lowercase + string.ascii_uppercase
for i in range(len(alphabets)):
    f=open('brutepem.pem','w')
    f.write(a+alphabets[i]+b)
    f.close()
    os.system('openssl rsautl -decrypt -in flag.enc -out output.txt -inkey brutepem.pem')
    with open('output.txt') as f2:
        if 'KCTF{' in f2.read():
            break