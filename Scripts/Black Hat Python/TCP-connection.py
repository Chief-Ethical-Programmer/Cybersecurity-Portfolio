#! /usr/bin/env python3
import socket
import argparse
import sys

def main():
    parser =argparse.ArgumentParser(prog="TCP-connection.py", description="CLI based TCP connection client") # initialization of the parser object 
    parser.add_argument("-t","--target", required=True, help="Target IP address or hostname")
    parser.add_argument("-p","--port", required=True, type=int, help="Target port")

    args = parser.parse_args() #for taking the arguments

    target_host = args.target
    target_port = args.port

    print(f"[+] Connecting to {target_host} on port {target_port}.....")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Creating an object where AF_INET means IPv4, SOCK_STREAM means TCP
            s.settimeout(5) # 5s wait time then retry
            s.connect((target_host, target_port))
            print("[+] Connection Established")
            request = f"GET / HTTP/1.1\r\nHost: {target_host}\r\nConnection: close\r\n\r\n"
            s.sendall(request.encode())
            response = b""
            while True:
                data = s.recv(4096)
                if not data: # empty values as false hence breaks the loop
                    break
                response += data
            print(response.decode("utf-8"))
    except Exception as e:
        print(f"[-] Connection Failed: {e}")
        sys.exit(1)

if __name__=="__main__":
    main()
