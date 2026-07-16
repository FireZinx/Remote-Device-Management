from infrastructure.compression.encode_image import EncodeImage
from domain.packet import PacketType

import asyncio
import time
import cv2

class GetCamera:
    def extract(self):
        while not self.close_threads:
            if not self.stream_cam_enabled:
                time.sleep(0.1)
                continue

            try:
                cap = cv2.VideoCapture(0)

                while not self.close_threads:
                    if not self.stream_cam_enabled:
                        break

                    self.event.wait()

                    ret, frame = cap.read()

                    if not ret or frame is None:
                        time.sleep(0.05)
                        continue

                    len_frame, frame_dump = EncodeImage.encode(frame)

                    self.queue.put_nowait(PacketType.CAMERA_STREAM + bytes([*len_frame]) + frame_dump)

                cap.release()
            except:
                asyncio.sleep(10)