#!/usr/bin/env python3
import socket
import ssl
import argparse

parser = argparse.ArgumentParser(description='Banner Grabber')
parser.add_argument('-t', '--target', required=True, help='Target IP')
args = parser.parse_args()

IP = args.target
Ports = [21, 22, 23, 25, 80, 443, 8080]

def grabber(IP, Ports):
    for Port in Ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((IP, Port))
                if Port == 443:
                    context = ssl.create_default_context()
                    s = context.wrap_socket(s, server_hostname=IP)
                if Port in [80, 443, 8080]:
                    request = f"GET / HTTP/1.1\r\nHost: {IP}\r\nConnection: close\r\n\r\n"
                    s.sendall(request.encode())
                banner = s.recv(1024).decode().strip()
                print(f"Banner for {IP}:{Port}: {banner}")
        except socket.error:
            print(f"Could not connect to {IP}:{Port}")

if __name__ == "__main__":
    grabber(IP, Ports)