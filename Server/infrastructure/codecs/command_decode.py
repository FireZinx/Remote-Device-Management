class DecodeData():
    def decode_message(protocol):
        length = int.from_bytes(Protocol.recv_packet(3), "big")

        data = b""
        while len(data) < length:
            data += Protocol.recv_packe(length - len(data))

        return data.decode("cp850")