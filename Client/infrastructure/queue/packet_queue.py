from queue import Queue, Empty 

class QueueClass:
    def __init__(self, event):
        self.queue = Queue()
        self.event = event

    def clear(self):
        while True:
            try:
                self.queue.get_nowait()
            except Empty:
                self.event.set()
                break

    def put_nowait(self, packet):
        self.queue.put_nowait(packet)

    def get(self):
        return self.queue.get()