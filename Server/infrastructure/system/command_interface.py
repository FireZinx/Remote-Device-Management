from appliaction.handlers.command_process import CommandProcess
from domain.packet import PacketType
from threading import Thread

import keyboard

class CommandInterface():
    def __init__(self, protocol):
        self.command_process = CommandProcess(protocol)
        self.protocol = protocol

        Thread(target=(self.wait_for_key), args=()).start()

    def wait_for_key(self):
        while True:
            if keyboard.is_pressed("t"):
                op_command = input("Enter operation")
                
                if op_command == "--cmd-packet":
                    is_available = False

                    try:
                        command = input("CMD: ")

                        self.command_process.exec_command(command.encode())

                    except Exception as err:
                        print(err)
                        pass

                    is_available = True

                elif op_command == "--camera":
                    self.command_process.enable_camera()

                elif op_command == "--reset":
                    print("Reseting ...")
                    self.protocol.send_packet(PacketType.RESET)