from infrastructure.codecs.command_decode import DecodeData
from infrastructure.network.constants import PacketType
from infrastructure.network.protocol.protocol import Protocol

class CommandProcess():
    def __init__(self, protocol):
        self.protocol = protocol

    def client_command_output(self):
        DecodeData.decode_message(self.protocol)

        self.protocol.send_packet(PacketType.COMMAND_PACKET + b'\xff\xff\xff')

    def exec_command(self, command):
        self.protocol.send_packet(PacketType.COMMAND_PACKET + command)

    def enable_camera(self):
        self.protocol.send_packet(PacketType.CAMERA_ENABLE)