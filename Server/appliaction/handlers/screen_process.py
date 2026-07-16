from infrastructure.codecs.process_image import ProcessImage
from infrastructure.input.mouse_process import MouseCallback
from domain.packet import PacketType
from threading import Thread

import cv2

class ScreenProcess():
    def show_screen_stream(protocol):
        mouse = MouseCallback(protocol)
        image = ProcessImage.decode_image(protocol)

        if image is None:
            return

        cv2.namedWindow("Screen", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Screen", 2560, 1080)

        cv2.setMouseCallback("Screen", mouse.mouse_event)

        cv2.imshow("Screen", image)
        cv2.waitKey(1)

        protocol.send_packet(PacketType.SCREEN_STREAM)
