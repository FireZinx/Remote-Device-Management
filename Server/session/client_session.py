class ClientSession():
    def __init__(self):
        self.client_address = []
        self.client = {}

    def insert_client(self, ddr, conn):
        self.client[ddr] = conn
        self.client_address.append(ddr)