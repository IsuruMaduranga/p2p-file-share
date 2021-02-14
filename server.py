import socket
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor

from routing import RoutingTable
from utils import query_builder, udp_send_recv
from FileHandler import search_file 

import constants as CONST


class UDPServer:

    def __init__(self, ip, port, dir, flask_port):
        self.ip = ip
        self.port = int(port)
        self.flask_port = flask_port
        self.dir = dir
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
            executor.submit(self._process_request, msg=msg, addr=addr, dir=self.dir, flask_ip=self.ip, flask_port=self.flask_port)

    def _process_request(self, msg, addr, dir, flask_ip, flask_port):
        msg = msg.decode("utf-8")
        tokens = msg.split()

        if tokens[1] == "JOIN":
            self.routing_table.add(tokens[2], tokens[3])
            response = query_builder("JOINOK", ["0"])
            udp_send_recv(addr[0], addr[1], response, recieve=False)

        elif tokens[1] == "LEAVE":
            for node in self.routing_table.get():
                if node[2] == tokens[3]:
                    self.routing_table.remove(node)
                    break

            response = query_builder("LEAVEOK", ["0"])
            udp_send_recv(addr[0], addr[1], response, recieve=False)

        elif tokens[1] == "SER":
            hops = int(tokens[5])
            files_found, file_names = search_file(dir, tokens[4])

            if files_found > 0:
                response = query_builder("SEROK", [files_found, flask_ip, flask_port, hops, file_names])
                udp_send_recv(tokens[2], tokens[3], response, recieve=False)

            elif hops > 0:
                request = query_builder("SER", [tokens[2], tokens[3], tokens[4], hops-1])
                for node in self.routing_table.get():
                    udp_send_recv(node[0], node[1], request, recieve=False)
        
        elif tokens[1] == "SEROK":
            print(">>>>>>>>>>>>>>>  Files Found: ", tokens[6:], " Flask IP: ", tokens[3], " Flask Port: ", tokens[4], "  <<<<<<<<<<<<<<<<<<<<")