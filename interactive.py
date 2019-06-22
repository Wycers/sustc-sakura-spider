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

base_time = " 12:00:00"

print(welcome_message)

print("using server @",host,":",port,"\n")

s = socket.socket()
s.connect((host, port))
sid = input("Enter Student ID: ")
pwd = getpass("Enter CAS Password: (Your input is hidden, Press [ENTER] after finish.)")
s.sendall(json.dumps({'action': 'login', 'username': sid, 'password': pwd}).encode())
JSESSIONID = json.loads(s.recv(1024).decode())['msg']
print("Trying to login...")
print("Login Result: JSESSIONID=",JSESSIONID,"\n")
s.close()

semester = input("Enter Semester (e.g. 2018-2019-2): ")
semester_base = input("Enter Semester Start Date (First Monday, e.g. 2019-02-18): ")
semester_base = semester_base + base_time
week_start = input("Enter Start Week: ")
week_end = input("Enter End Week: (Including)")

s2 = socket.socket()
s2.connect((host, port))
s2.sendall(json.dumps({'action': 'trans', 'JSESSIONID': JSESSIONID, 'semester':semester,'semester_base':semester_base,'week_start':week_start,'week_end':week_end}).encode())
print(s2.recv(1024).decode())