#! /usr/bin/env python3
import socket
target = "www.google.com"
port = 80

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creatiing an object where AF_INET means IPv4, SOCK_STREAM means TCP
s.connect((target, port))
s.send(b"GET / HTTP/1.1\r\nHost: www.google.com\r\nConnection: close\r\n\r\n") #Connection: close is used to close the connection after the response is received
response = b"" #empty string to store the response
while True:
    data = s.recv(4096)
    if not data: #empty values as false hences breaks the loop
        break
    response+=data
print(response.decode("utf-8"))
s.close()
