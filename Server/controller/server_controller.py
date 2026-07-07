from workers.command_process import CommandProcess
from workers.camera_process import CameraProcess
from workers.screen_process import ScreenProcess
from network.constants import PacketType
from multiprocessing import Process

import time
import psutil
import os

class ServerController():
    def __init__(self, protocol, is_available):
        self.is_available = is_available
        self.protocol = protocol

        Process(target=(self.process_packet), args=()).start()

    def process_packet(self):
        process = psutil.Process()
        process.cpu_affinity({0, 1, 2, 3, 4, 5})

        while True:
            if not self.is_available:
                time.sleep(0.1)
                continue

            try:
                packet_client = self.protocol.recv_packet(1)

                if packet_client == PacketType.CAMERA_STREAM:
                    CameraProcess.show_cam_stream(self.protocol)

                elif packet_client == PacketType.SCREEN_STREAM:
                    ScreenProcess.show_screen_stream(self.protocol)

                elif packet_client == PacketType.COMMAND_PACKET:
                    CommandProcess.client_command_output()

            except Exception as err:
                print(err)
                continue