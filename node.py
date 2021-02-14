import sys
import random
import os
import shutil

from cli import CLI
from server import UDPServer
from api import RESTServer
from utils import query_builder, udp_send_recv, query_parser, generate_random_file
from routing import RoutingTable

class Node:

    def __init__(self, udp_ip, udp_port, flask_port, username, bs_ip, bs_port):

        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.flask_port = flask_port
        self.username = username
        self.dir = "data/" + username
        self.bs_ip = bs_ip
        self.bs_port = bs_port

        self.routing_table = RoutingTable()
        self.cli = CLI(self.dir, self.udp_ip, self.udp_port)
        self.udp_server = UDPServer(self.udp_ip, self.udp_port, self.dir, self.flask_port)
        self.rest_server = RESTServer(self.flask_port)

    def run(self):

        # generate random files to be shared
        self.generate_files(random.randint(2, 5))

        self.reg_in_bs()
        self.connect_to_network()

        # starting udp server in a new process
        self.udp_server.run()

        # starting rest server in a new process
        self.rest_server.run()

        # starting cli in the main process
        self.cli.run()

        self.udp_server.terminate()
        self.rest_server.terminate()

        self.unreg_from_bs()
        self.disconnect_from_network()
        shutil.rmtree(self.dir)

    def reg_in_bs(self):

        query = query_builder("REG", data=[self.udp_ip, self.udp_port, self.username])
        data = udp_send_recv(self.bs_ip, self.bs_port, query)
        
        try:
            res_type, data = query_parser(data)
        except Exception as e:
            print("Error:", str(e))
            sys.exit("Exiting, Couldn't connect to BS")
        else:
            if res_type == "REGOK":
                for i in range(0, len(data), 2):
                    self.routing_table.add(data[i], data[i + 1])
            else:
                print("Error: Invalid response from BS")
                sys.exit("Exiting, Couldn't connect to BS")

    def unreg_from_bs(self):

        query = query_builder("UNREG", data=[self.udp_ip, self.udp_port, self.username])
        res = udp_send_recv(self.bs_ip, self.bs_port, query)

        try:
            res_type, res = query_parser(res)
        except Exception as e:
            pass

    def connect_to_network(self):
        for ip,port in self.routing_table.get():
            query = query_builder("JOIN", data=[self.udp_ip, self.udp_port])
            data = udp_send_recv(ip, port, query)
            try:
                res_type, data = query_parser(data)
            except Exception as e:
                print("Error:", str(e))
                self.routing_table.remove((ip, port))
            else: 
                if res_type == "JOINOK":
                    print("JOINED")
                   

    def disconnect_from_network(self):
        for ip,port in self.routing_table.get():
            query = query_builder("LEAVE", data=[self.udp_ip, self.udp_port])
            data = udp_send_recv(ip, port, query)
            try:
                res_type, data = query_parser(data)
            except Exception as e:
                print("Error:", str(e))
            else: 
                if res_type == "LEAVEOK":
                    print("LEAVED")
    
    def generate_files(self, num_files):
        os.mkdir(self.dir) 

        print(f"Generating {num_files} files")

        file_names = []
        with open("data/File Names.txt", 'r') as in_file:
            for line in in_file:
                file_names.append(line.strip())
        random.shuffle(file_names)

        for i in range(num_files):
            generate_random_file(self.dir, file_names[i], random.randint(2, 10))

if __name__ == "__main__":
    args = sys.argv[1:]
    node = Node(args[0], args[1], args[2], args[3], args[4], args[5])
    node_data = node.run()