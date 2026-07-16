from infrastructure.codecs.process_image import ProcessImage
from domain.packet import PacketType
from threading import Thread

import cv2

class CameraProcess():
    def show_cam_stream(protocol): 
        image = ProcessImage.decode_image(protocol)

        if image is None:
            return

        cv2.namedWindow("Stream", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Stream", 1280, 720)

        cv2.imshow("Stream", image)
        cv2.waitKey(1)

        protocol.send_packet(PacketType.CAMERA_STREAM)