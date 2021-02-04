import socket
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor
from utils import query_builder, udp_send_recv
from routing import RoutingTable

import constants as CONST


class UDPServer:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.ip, self.port))
        self.server_process = Process(target=self._start)
        self.routing_table = RoutingTable()

    def run(self):
        self.server_process.start()

    def terminate(self):
        self.server_process.terminate()

    def _start(self):
        executor = ThreadPoolExecutor(max_workers=3)
        while True:
            msg, addr = self.server.recvfrom(CONST.BUFFER_SIZE)
            executor.submit(self._process_request, msg=msg, addr=addr)

    def _process_request(self, msg, addr):
        msg = msg.decode("utf-8")
        toks = msg.split()

        if toks[1] == "JOIN":
            self.routing_table.add(toks[2], toks[3])
            response = query_builder("JOINOK", ["0"])
            udp_send_recv(addr[0], addr[1], response, recieve=False)

        elif toks[1] == "LEAVE":
            for node in self.routing_table.get():
                if node[2] == int(toks[3]):
                    self.routing_table.remove(node)
                    break

            response = query_builder("LEAVEOK", ["0"])
            udp_send_recv(addr[0], addr[1], response, recieve=False)

        elif toks[1] == "SER":
            current_hop = int(toks[5])
            files_found = 0
            file_names = ""

            '''  TODO
            First search in the local storage, if found increment the fileFound varibale,
			for file in FD.files:
				if toks[4].replace("-", " ") in file:
					filesFound+=1
					fileNames += " " + file
            '''

            # if files are found send response back, no need to ask from his neighbours
            if files_found > 0:
                response = query_builder("SEROK", [files_found, self.ip, self.port, current_hop, file_names])
                udp_send_recv(addr[0], addr[1], response, recieve=False)

            elif current_hop > 0:
                request = query_builder("SER", [toks[2], toks[3], toks[4], current_hop - 1])
                for node in self.routing_table.get():
                    udp_send_recv(node[0], node[1], request, recieve=False)
