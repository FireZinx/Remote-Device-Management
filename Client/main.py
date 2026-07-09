from infrastructure.controller.client_controller import ClientController
from infrastructure.network.client_receiver import ClientReceiver
from infrastructure.network.client import Client
from infrastructure.queue.packet_queue import QueueClass
from worker.generate_threads import GenerateThreads
from threading import Event
import time

class Application():
    def __init__(self):
        self.mouse_pos = [0, 0]
        self.mouse_click = None
        self.client = None
        self.event = None
        self.queue = None

        self.start()
        
    def start(self):
        while True:
            print("Attempting to connect to server...")

            self.event = Event()
            self.queue = QueueClass(self.event)

            try:
                self.stream_cam_enabled = False
                self.close_threads = False

                self.client = Client.start(self)

                self.queue.clear()

                self.threads = GenerateThreads.create(self)

                print("test")
                
                self.client_controller = ClientController.start(self)

            except Exception as err:
                time.sleep(5)
                continue

if __name__ == "__main__":
    Application()