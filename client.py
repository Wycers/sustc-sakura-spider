"""mock client to test spider server
"""

import socket
import json
host = '127.0.0.1'
port = 9090

s = socket.socket()
s.connect((host, port))
s.sendall(json.dumps({'action': 'login', 'username': '11711918', 'password': '301914'}).encode())
JSESSIONID = json.loads(s.recv(1024).decode())['msg']
print(JSESSIONID)
s.close()

s2 = socket.socket()
s2.connect((host, port))
s2.sendall(json.dumps({'action': 'trans', 'JSESSIONID': JSESSIONID}).encode())
print(s2.recv(1024).decode())
