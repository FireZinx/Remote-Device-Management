from infrastructure.network.client_receiver import ClientReceiver
from infrastructure.system.command_process import Command
from capture.generate_threads import GenerateThreads
from domain.packet import PacketType
from capture.mouse import Mouse

import os
import sys
import time

class ClientController():
    def start(self):
        while not self.close_threads:
            try:
                packet = ClientReceiver.recv_packet(self)

                if packet[1:4] != b'\xff\xff\xff':
                    if packet[:1] == PacketType.COMMAND_PACKET:
                        Command.execute(packet[1:])

                    elif packet[:1] == PacketType.MOUSE_PACKET:
                        self.mouse_click = packet[1:2]
                        self.mouse_pos = [int.from_bytes(packet[2:4], "big"), int.from_bytes(packet[4:6], "big")]

                    elif packet[:1] == PacketType.CAMERA_ENABLE:
                        if not self.stream_cam_enabled:
                            self.stream_cam_enabled = True
                        else:
                            self.stream_cam_enabled = False

                    elif packet[:1] == PacketType.SCREEN_STREAM:
                        self.event.set()

                    elif packet[:1] == PacketType.RESET:
                        self.queue.clear()

                else:
                    self.queue.clear()

            except Exception as err:
                self.close_threads = True