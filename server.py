import socket
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor

from routing import RoutingTable
from utils import query_builder, udp_send_recv
from FileHandler import search_file 
from threading import Lock

import constants as CONST

import configuration as cfg


class UDPServer:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.ip, self.port))
        self.server_process = Process(target=self._start)
        self.routing_table = RoutingTable()
        self.lock = Lock()

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

        if tokens[1] == "JOIN":
            self.routing_table.add(tokens[2], tokens[3])
            response = query_builder("JOINOK", ["0"])
            udp_send_recv(addr[0], addr[1], response, recieve=False)

        elif tokens[1] == "LEAVE":
            for node in self.routing_table.get():
                if node[1] == tokens[3]:
                    self.routing_table.remove(node)
                    break
            response = query_builder("LEAVEOK", ["0"])
            udp_send_recv(addr[0], addr[1], response, recieve=False)

        elif tokens[1] == "SER":
            hops = int(tokens[-1])
            file_name = " ".join(tokens[4:-1])
            files_found, file_names = search_file(file_name)

            if files_found > 0:
                response = query_builder("SEROK", [files_found, cfg.FlaskServer['ip'], cfg.FlaskServer['port'], hops, file_names])
                udp_send_recv(tokens[2], tokens[3], response, recieve=False)

            elif hops > 0:
                request = query_builder("SER", [tokens[2], tokens[3], file_name, hops-1])
                for node in self.routing_table.get():
                    udp_send_recv(node[0], node[1], request, recieve=False)
        
        elif tokens[1] == "SEROK":
            dir = cfg.Application['dir'] 
            films = " ".join(tokens[6:]).strip()

            self.lock.acquire()
            f = open(f"{dir}/film_details.txt", "a")
            file1 = open(f"{dir}/film_details.txt")

            for film in films.split(','):
                found = False
                for line in file1.readlines():
                    if film in line:
                        found = True
                if not found:
                    print(f"\t* {film}")
                    f.write(f"{film}|{tokens[3]}|{tokens[4]}\n")
                    
            f.close()
            file1.close()
            self.lock.release()