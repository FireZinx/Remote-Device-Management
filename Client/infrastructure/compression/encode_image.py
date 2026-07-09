import cv2

class EncodeImage():
    def encode(image):
        _, encoded = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 100])

        frame_dump = encoded.tobytes()
        dump_len = len(frame_dump)

        len_frame = [(dump_len >> 16) & 0xff, (dump_len >> 8) & 0xff, dump_len & 0xff]

        return len_frame, frame_dump