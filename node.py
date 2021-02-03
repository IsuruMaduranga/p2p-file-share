from cli import CLI
from server import UDPServer
from api import RESTServer
from utils import query_builder,udp_send_recv,query_parser
from routing import RoutingTable
import sys

class Node:

    def __init__ (self,ip,port,username,bs_ip,bs_port):

        self.ip = ip
        self.port = port
        self.username = username

        self.bs_ip = bs_ip
        self.bs_port = bs_port

        self.routing_table = RoutingTable()
        self.cli = CLI()
        self.udp_server = UDPServer()
        self.rest_server = RESTServer()

    
    def run(self):

        self.reg_in_bs()
        self.connect_to_network()

        # strating udp server in a new thread
        self.udp_server.run()

        # starting rest server in a new thread
        self.rest_server.run()

        # starting cli in the main thread
        self.cli.run()

        self.udp_server.join()
        self.rest_server.join()

        self.unreg_from_bs()
        self.disconnect_from_network()

    def reg_in_bs(self):
        # to be implemented
        pass


    def unreg_from_bs(self):
        # to be implemented
        pass

    def connect_to_network(self):
        # to be implemented
        pass

    def disconnect_from_network(self):
        # to be implemented
        pass




if __name__ == "__main__":

    node = Node("127.0.0.1",5001,"node2","127.0.0.1",55555)
    data = node.run()