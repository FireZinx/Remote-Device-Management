from infrastructure.network.protocol.protocol import Protocol
from appliaction.session.client_session import ClientSession
from infrastructure.system.select_client import SelectClient
from threading import Thread
from server import Server

import asyncio

class Application():
    def __init__(self):
        self.client_session = ClientSession()
        self.select_host = SelectClient()
        self.protocol = Protocol()
        self.server = Server(self.client_session)

        self.select_host.start(self.client_session, self.protocol)
        
if __name__ == "__main__":
    Application()