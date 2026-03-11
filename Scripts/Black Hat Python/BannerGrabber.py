#!/usr/bin/env python3
import socket
import ssl
import argparse

#To take cli arguments for the target IP address
parser = argparse.ArgumentParser(description='Banner Grabber')
parser.add_argument('-t', '--target', required=True, help='Target IP')
args = parser.parse_args()

IP = args.target
Ports = [21, 22, 23, 25, 53, 80, 443, 8080, 4444] # All the common ports to grab banners from the host

# Function to grab banners from the specified ports
def grabber(IP, Ports):
    for Port in Ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((IP, Port))

                if Port == 443: 
                    context = ssl.create_default_context()
                    context.check_hostname = False # Disabling hostname checking for self-signed certificates
                    context.verify_mode = ssl.CERT_NONE # Disabling certificate verification for self-signed certificates
                    s = context.wrap_socket(s, server_hostname=IP) # Wrapping the socket with ssl for secure connection 
                if Port in [80, 443, 8080]: # Sending HTTP request to grab the banner from the web server
                    request = f"GET / HTTP/1.1\r\nHost: {IP}\r\nConnection: close\r\n\r\n"
                    s.sendall(request.encode())
                banner = s.recv(1024).decode()
                print(f"Banner for {IP}:{Port}: {banner} \n")
        except socket.error:
            print(f"Could not connect to {IP}:{Port}")

if __name__ == "__main__":
    grabber(IP, Ports)