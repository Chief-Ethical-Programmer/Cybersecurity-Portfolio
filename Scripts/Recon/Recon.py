import socket

domain = input("Enter the domain to scan: ")
class Prey:
    def __init__(self,domain):
        self.domain=domain

    def scan(self):
        self.ip=socket.gethostbyname(self.domain)   # gethostbyname is a function class socket
        return self.ip
    
    def port_scan(self):
        self.ports=[21,443,80,22,25,8080,8888]
        self.port=[]
        for i in self.ports:
            s=socket.socket() # A temporary port with my ip is opened where OS is listening
            result = s.connect_ex((self.ip,i)) # Here I am using the connect_ex() function via object of the socket
            if result==0:
                self.port.append(i)
            s.close()
        return self.port

t=Prey(domain)
print(f"Ip address of the {domain}: {t.scan()}") 
print(f"Open ports are:{t.port_scan()}") 
