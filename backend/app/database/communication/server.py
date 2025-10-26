import socket
import struct

class SocketServer:
    def __init__(self, client_address, client_port = 80):
        self.client_address = client_address
        self.client_port = client_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.client_address, self.client_port))
    
    def __str__(self):
        return f"client_address: {self.client_address}, client_port: {self.client_port}"
    
    def send(self, data):
        data = bytes(data, "utf-8")
        self.sock.sendto(data, (self.client_address, self.client_port))

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()