"""mock client to test spider server
"""

import socket
import json
host = '127.0.0.1'
port = 9090

s = socket.socket()
s.connect((host, port))
s.sendall(json.dumps({'action': 'login', 'username': 'sid_here', 'password': 'pwd_here'}).encode())
JSESSIONID = json.loads(s.recv(1024).decode())['msg']
print(JSESSIONID)
s.close()

s2 = socket.socket()
s2.connect((host, port))
s2.sendall(json.dumps({'action': 'trans', 'JSESSIONID': JSESSIONID, 'semester':'2018-2019-2','semester_base':'2019-02-18 12:00:00','week':1}).encode())
print(s2.recv(1024).decode())
