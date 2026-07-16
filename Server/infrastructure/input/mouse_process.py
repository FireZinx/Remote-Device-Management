from domain.packet import PacketType

import cv2

class MouseCallback():
    def __init__(self, protocol):
        self.protocol = protocol

    def _encode_coord(self, value):
        value = max(0, min(int(value), 65535))
        return value.to_bytes(2, "big")

    def mouse_event(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.protocol.send_packet(PacketType.MOUSE_PACKET + PacketType.LMOUSEBUTTON + self._encode_coord(x) + self._encode_coord(y))

        elif event == cv2.EVENT_RBUTTONDOWN:
            self.protocol.send_packet(PacketType.MOUSE_PACKET + PacketType.RMOUSEBUTTON + self._encode_coord(x) + self._encode_coord(y))

        elif event == cv2.EVENT_MOUSEMOVE:
            pass