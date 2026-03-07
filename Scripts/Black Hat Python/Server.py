#!/usr/bin/env python3
import socket
import threading

def handle_client(client):
    with client as c:
        try:
            request = c.recv(4096).decode('utf-8')
            print(f"[+] Received: {request}")
            c.send(b'Hello from the Server :)') # send acknowledgment back to the client
        except Exception as e:
            print(f"[-] Error handling client: {e}")


def main():
    bind_host = '0.0.0.0' # Listen on everything
    bind_port = 4444
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_host, bind_port))
    server.listen(5)  # Listen for up to 5 connections
    print(f"[+] Listening on {bind_host} : {bind_port}")
    while True:
        client, addr = server.accept() # accept() waits until a connection is made
        print(f"[+] Accepted connection from {addr[0]} : {addr[1]}") 

        # Threading to handle multiple clients simultaneously
        t = threading.Thread(target=handle_client, args=(client,)) 
        t.start()

if __name__=='__main__':
    main()