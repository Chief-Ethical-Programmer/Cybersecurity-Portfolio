import socket

domain = input("Enter the domain to scan: ")
class Prey:
    def __init__(self,domain):
        self.domain=domain

    def scan(self):
        self.ip=socket.gethostbyname(self.domain)  
        return self.ip
t=Prey(domain)
print(f"Ip address of the {domain}: {t.scan()}") 