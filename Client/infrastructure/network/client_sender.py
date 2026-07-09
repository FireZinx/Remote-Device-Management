
class ClientSend:
    def start(self):
        while not self.close_threads:
            try:
                packet = self.queue.get()

                if packet:
                    self.client.sendall(packet)
            except:
                break