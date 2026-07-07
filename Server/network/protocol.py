class Protocol:
    def __init__(self):
        self.conn = None

    def start(self, conn):
        self.conn = conn

    def recv_packet(self, lenght):
        data = self.conn.recv(lenght)
        return data

    def send_packet(self, packet):
        self.conn.sendall(packet)