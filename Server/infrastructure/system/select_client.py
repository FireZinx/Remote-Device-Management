from controller.server_controller import ServerController
from infrastructure.system.command_interface import CommandInterface

class SelectClient:
    def start(self, client_session, protocol):
        while True:
            print("Ip list: ", client_session.client_address)

            try:
                device = input("Select: ")

                conn = client_session.client[device]

                protocol.start(conn)
                ServerController(protocol)
                CommandInterface(protocol)

                break

            except Exception as err:
                print(err)
                continue