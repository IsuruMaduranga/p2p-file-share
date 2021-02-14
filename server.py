import socket
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor

from routing import RoutingTable
from utils import query_builder, udp_send_recv
from request_handler import process_request

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
        tokens = msg.split()

        processed_request = process_request(tokens)

        if processed_request['request'] == "JOIN":
            self.routing_table.add(tokens[2], tokens[3])
            response = query_builder("JOINOK", ["0"])
            udp_send_recv(addr[0], addr[1], response, recieve=False)

        elif processed_request['request'] == "LEAVE":
            for node in self.routing_table.get():
                if node[2] == int(tokens[3]):
                    self.routing_table.remove(node)
                    break

            response = query_builder("LEAVEOK", ["0"])
            udp_send_recv(addr[0], addr[1], response, recieve=False)

        elif processed_request['request'] == "SER":
            files_found = processed_request['file_found']
            hop_count = processed_request['hop_count']

            if files_found > 0:
                response = query_builder("SEROK",
                                         [files_found, self.ip, self.port, hop_count, processed_request['file_names']])
                udp_send_recv(addr[0], addr[1], response, recieve=False)

            elif hop_count > 0:
                request = query_builder("SER", [tokens[2], tokens[3], tokens[4], hop_count])
                for node in self.routing_table.get():
                    udp_send_recv(node[0], node[1], request, recieve=False)
