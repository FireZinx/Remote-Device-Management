from interface.command_interface import CommandInterface
from controller.server_controller import ServerController
from session.client_session import ClientSession

class SelectHost:
    def start(self, client_session, Protocol):
        is_available = True

        while True:
            print("Ip list: ", client_session.client_address)

            try:
                device = input("Select: ")

                conn = client_session.client[device]

                Protocol.start(conn)
                ServerController(Protocol, is_available)
                CommandInterface(Protocol, is_available)

                break
  
            except Exception as err:
                print(err)
                continue