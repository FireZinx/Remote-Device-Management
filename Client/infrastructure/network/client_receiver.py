class ClientReceiver():
    def recv_packet(self):
        try:
            data = self.client.recv(1024)
            return data
            
        except:
            return