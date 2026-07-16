from appliaction.session.handle_session import SessionHandler
from threading import Thread

import socket

class Server:
    def __init__(self, client_session):
        self.client_session = client_session

        Thread(target=self.start, args=()).start()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("0.0.0.0", 4000))
        self.server.listen(10)

        SessionHandler.start(self.server, self.client_session)
