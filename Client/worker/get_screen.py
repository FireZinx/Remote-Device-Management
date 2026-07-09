from infrastructure.compression.encode_image import EncodeImage
from infrastructure.network.constants import PacketType
from PIL import ImageGrab

import cv2
import numpy

class GetScreen:
    def extract(self):
        try:
            while not self.close_threads:
                self.event.wait()

                img_array = numpy.array(ImageGrab.grab())
                img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

                len_frame, frame_dump = EncodeImage.encode(img)

                self.queue.put_nowait(PacketType.SCREEN_STREAM + bytes([*len_frame]) + frame_dump)

        except:
            return
