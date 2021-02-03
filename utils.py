from exceptions import MessageLengthError,ResponseError,InvalidQueryError
from constants import HEADER_LENGTH,BUFFER_SIZE,RESPONSE_CODES
import socket

def query_builder(type,data):

    query = " " + " ".join([type] + list(map(str,data)))

    if(len(query)>9995):
        raise MessageLengthError("Maximum message length exceeded")
    else:
        query = str(len(query) + HEADER_LENGTH).zfill(4) + query

    return bytes(query,"utf-8")

def query_parser(query):

    query = query.split(" ")
    res_type = query[0]
    res_code = query[1]

    if res_type in RESPONSE_CODES and res_code in RESPONSE_CODES[res_type]:
        
        code = RESPONSE_CODES[res_type][res_code]

        if code["stat"]:
            return query[0],query[2:]
        else:
            raise ResponseError(code["msg"])
    else:
        raise InvalidQueryError


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
    print(query_builder("REG",["129.82.123.45","5001","1234abcd"]).decode("utf-8"))
    print(query_builder("REGOK",["2","129.82.123.45","5001","64.12.123.190","34001"]).decode("utf-8"))