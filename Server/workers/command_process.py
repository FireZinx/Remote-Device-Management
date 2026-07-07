from network.constants import PacketType
from network.protocol import Protocol

class CommandProcess():
    def __init__(self, protocol):
        self.protocol = protocol

    def client_command_output(self):
        length = int.from_bytes(Protocol.recv_packet(3), "big")

        data = b""
        while len(data) < length:
            data += Protocol.recv_packe(length - len(data))

        print("data: ", data.decode("cp850"))

        self.protocol.send_packet(COMMAND_PACKET + b'\xff\xff\xff')

    def exec_command(self, command):
        self.protocol.send_packet(PacketType.COMMAND_PACKET + command)

    def enable_camera(self):
        self.protocol.send_packet(PacketType.CAMERA_ENABLE)