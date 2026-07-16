from appliaction.handlers.command_process import CommandProcess
from threading import Thread

import keyboard

class CommandInterface():
    def __init__(self, protocol, is_available):
        self.command_process = CommandProcess(protocol)
        self.is_available = is_available
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
                    CommandProcess.enable_camera()