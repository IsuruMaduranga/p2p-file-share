import socket
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor

import constants as CONST

class UDPServer:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.ip, self.port))
        self.server_process = Process(target=self._start)

    def run(self):
        self.server_process.start()

    def join(self):
        self.server_process.terminate()
        
    def _start(self):
        executor = ThreadPoolExecutor(max_workers=3)
        while True:
            msg, addr = self.server.recvfrom(CONST.BUFFER_SIZE)
            executor.submit(self.__processRequest, msg=msg, addr=addr)
    
    def __processRequest(self, msg, addr):
        msg = msg.decode("utf-8")
        toks = msg.split()
        print(msg)
        # toks[0] <- length of the request body
        # toks[1] <-  protocol (JOIN/SER/REG/UNREG/LEAVE)
        # toks[1,2....] <- other info
        pass