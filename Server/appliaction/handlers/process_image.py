import numpy as np
import cv2

class ProcessImage():
    def decode_image(protocol):
        packet_len = int.from_bytes(protocol.recv_packet(3), "big")

        cameraDump = b""

        while len(cameraDump) < packet_len:
            cameraDump += protocol.recv_packet(packet_len - len(cameraDump))

        image_decoded = cv2.imdecode(np.frombuffer(cameraDump, dtype=np.uint8), cv2.IMREAD_COLOR)

        return image_decoded