import socket
from constants import HEADER_LENGTH,BUFFER_SIZE,RESPONSE_CODES
from exceptions import MessageLengthError

def query_builder(type,data):

    query = " " + " ".join([type] + list(map(str,data)))

    if(len(query)>9995):
        raise MessageLengthError("Maximum message length exceeded")
    else:
        query = str(len(query) + HEADER_LENGTH).zfill(4) + query

    return bytes(query,"utf-8")

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