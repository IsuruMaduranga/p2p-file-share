#from cli import CLI
from server import UDPServer
from api import RESTServer
from utils import query_builder,udp_send_recv,query_parser
from routing import RoutingTable
import sys

class Node:

    def __init__ (self, udp_ip, udp_port, flask_port, username, bs_ip, bs_port):

        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.flask_port = flask_port
        self.username = username

        self.bs_ip = bs_ip
        self.bs_port = bs_port

        self.routing_table = RoutingTable()
        #self.cli = CLI()
        self.udp_server = UDPServer(self.udp_ip, self.udp_port)
        self.rest_server = RESTServer(self.flask_port)

    
    def run(self):

        self.reg_in_bs()
        self.connect_to_network()

        # strating udp server in a new process
        self.udp_server.run()

        # starting rest server in a new process
        self.rest_server.run()

        # starting cli in the main process
        #self.cli.run()

        self.udp_server.terminate()
        self.rest_server.terminate()

        self.unreg_from_bs()
        self.disconnect_from_network()

    def reg_in_bs(self):
        
        query = query_builder("REG",data=[self.udp_ip,self.udp_port,self.username])
        data = udp_send_recv(self.bs_ip,self.bs_port,query)

        try:
            res_type,data = query_parser(data)
        except Exception as e:
            print("Error:",str(e))
            sys.exit('Exiting, Couldn\'t connect to BS')
        else:
            if res_type == "REGOK":
                for i in range(0,len(data),2):
                    self.routing_table.add(data[i],data[i+1])
            else:
                print("Error: Invalid response from BS")
                sys.exit('Exiting, Couldn\'t connect to BS')


    def unreg_from_bs(self):
        # to be implemented
        pass

    def connect_to_network(self):
        # to be implemented
        pass

    def disconnect_from_network(self):
        # to be implemented
        pass

