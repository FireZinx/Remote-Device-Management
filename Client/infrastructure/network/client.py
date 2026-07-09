import socket
import time

class Client():
    def start(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("192.168.15.3", 4000))

        return self.client