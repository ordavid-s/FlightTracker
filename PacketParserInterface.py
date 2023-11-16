import os
import threading
import json


class PacketParserInterface:
    def __init__(self, pcap_path, pipe_path, parser_path="./PacketParser"):
        self.callbacks = []
        self.pipe_path = pipe_path
        self.pcap_path = pcap_path
        self.parser_path = parser_path
        self.lock = threading.Lock()
        try:
            os.mkfifo(pipe_path)
        except OSError:  # pipe exists try again
            os.unlink(pipe_path)
            os.mkfifo(pipe_path)

    def _process_line(self, line):
        line = line.replace("True", "true")
        line = line.replace("False", "false")
        line = line.replace("'", '"')
        return line

    def register_callback(self, cb):
        self.callbacks.append(cb)

    def _start_streaming(self):
        os.system(f"{self.parser_path} pcap {self.pcap_path} {self.pipe_path}")

    def read_data(self):
        self.lock.acquire()
        threading.Thread(target=self._start_streaming).start()
        with open(self.pipe_path, 'r') as fifo:
            while True:
                line = fifo.readline()
                if line == "END\n":
                    break
                line = self._process_line(line)
                data = json.loads(line)
                for cb in self.callbacks:
                    cb.run(data)

    def clean(self):
        os.unlink(self.pipe_path)

class PrintCallback:
    def __init__(self):
        pass

    def run(self, pkt):
        print(pkt)


if __name__ == '__main__':
    # Open the named pipe for reading
    path = "/home/ordavid/Desktop/PacketParser/mypipe"
    file_path = "./resources/long.pcap"
    pi = PacketParserInterface(file_path, path)
    pi.register_callback(PrintCallback())
    pi.read_data()
    pi.clean()
