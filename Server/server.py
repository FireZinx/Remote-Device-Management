from controller.server_controller import ServerController
from interface.select_host import SelectHost
from session.client_session import ClientSession

import socket

class Server:
    def __init__(self, client_session):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("0.0.0.0", 4000))
        self.server.listen(10)

        self.client_session = client_session

    def start(self):
        while True:
            conn, addr = self.server.accept()
            ddr = addr[0]+":"+str(addr[1])

            print("Connection recv: ", ddr)

            self.client_session.insert_client(ddr, conn)
