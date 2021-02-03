import socket
from constants import HEADER_LENGTH,BUFFER_SIZE,RESPONSE_CODES

def query_builder(type,data):
    # to be implemented
    pass

def query_parser(query):
    # to be implemented
    pass

def udp_recv(sock):

    data = sock.recv(BUFFER_SIZE)
    sock.close()
    return data.decode("utf-8")[5:]

def udp_send_recv(ip,port,data,recieve=True):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((ip, port))
    s.send(data)

    data = ""
    if recieve:
        return udp_recv(s)

if __name__ == "__main__":

    # quick unit tests
    pass