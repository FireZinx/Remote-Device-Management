from workers.command_process import CommandProcess
from session.client_session import ClientSession
from interface.select_host import SelectHost
from network.protocol import Protocol
from threading import Thread
from server import Server

class Application():
    def __init__(self):
        self.client_session = ClientSession()
        self.select_host = SelectHost()
        self.protocol = Protocol()
        self.server = Server(self.client_session)

        Thread(target=(self.server.start), args=()).start()

        self.select_host.start(self.client_session, self.protocol)
if __name__ == "__main__":
    Application()