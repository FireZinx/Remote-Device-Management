from infrastructure.network.client_sender import ClientSend
from worker.get_camera import GetCamera
from worker.get_screen import GetScreen
from worker.redirect_mouse import Mouse
from threading import Thread

class GenerateThreads:
    def create(self):
        threads = [
            Thread(target=GetScreen.extract, args=(self,), daemon=True),
            Thread(target=GetCamera.extract, args=(self,), daemon=True),
            Thread(target=Mouse.redirect, args=(self,), daemon=True),
            Thread(target=ClientSend.start, args=(self,), daemon=True),
        ]

        for workers in threads:
            workers.start()

        return threads