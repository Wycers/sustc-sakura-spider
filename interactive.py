"""interactive interface
"""

import socket
import json
from getpass import getpass
host = '127.0.0.1'
port = 9090

welcome_message = """sustc-sakura-spider / Course2iCal
Created by Wycers & Nekonull
We don't store your CAS information."""

print(welcome_message)

print("using server @",host,":",port,"\n")

s = socket.socket()
s.connect((host, port))
sid = input("Enter Student ID: ")
pwd = getpass("Enter CAS Password: ")
s.sendall(json.dumps({'action': 'login', 'username': sid, 'password': pwd}).encode())
JSESSIONID = json.loads(s.recv(1024).decode())['msg']
print("\nLogin success! JSESSIONID=",JSESSIONID)
s.close()

s2 = socket.socket()
s2.connect((host, port))
s2.sendall(json.dumps({'action': 'trans', 'JSESSIONID': JSESSIONID, 'semester':'2018-2019-2','semester_base':'2019-02-18 12:00:00','week':1}).encode())
print(s2.recv(1024).decode())