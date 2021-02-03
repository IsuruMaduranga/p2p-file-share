
class Node:

    def __init__ (self,ip,port,username,bs_ip,bs_port):
        # to be implemented
        pass

    
    def run(self):
        # to be implemented
        pass

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