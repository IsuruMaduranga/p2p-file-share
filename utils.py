import os
import socket

from exceptions import MessageLengthError, ResponseError, InvalidQueryError
from constants import HEADER_LENGTH, BUFFER_SIZE, RESPONSE_CODES


def query_builder(query_type, data):
    query = " " + " ".join([query_type] + list(map(str, data)))

    if len(query) > 9995:
        raise MessageLengthError("Maximum message length exceeded")
    else:
        query = str(len(query) + HEADER_LENGTH).zfill(4) + query

    return bytes(query, "utf-8")


def query_parser(query):
    query = query.decode("utf-8")
    query = query.split(" ")
    res_type = query[1]
    res_code = query[2]

    if res_type in RESPONSE_CODES and res_code in RESPONSE_CODES[res_type]:

        code = RESPONSE_CODES[res_type][res_code]

        if code["stat"]:
            return query[1], query[3:]
        else:
            raise ResponseError(code["msg"])
    else:
        raise InvalidQueryError


def udp_recv(sock):
    data, addr = sock.recvfrom(BUFFER_SIZE)
    sock.close()
    return data


def udp_send_recv(ip, port, data, recieve=True):
    port = int(port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(data, (ip, port))
    data = ""
    if recieve:
        return udp_recv(s)

    s.close()


def generate_byte_array(array_size):
    lower_bound = ord(b'0')
    length = 10
    # print(array_size)
    # Generate a random array of length array_size and assign integers based on the array
    byte_array = bytearray(os.urandom(array_size))
    for i, b in enumerate(byte_array):
        byte_array[i] = lower_bound + b % length

    return byte_array


def generate_random_file(dir, file_name, file_size):
    num_bytes = 1024 * 1024 * file_size
    random_integer = generate_byte_array(num_bytes)

    if os.path.exists(dir):
        with open(os.path.join(dir + "/" + file_name), "wb") as out_file:
            out_file.write(random_integer)


if __name__ == "__main__":
    # quick unit tests
    print(query_builder("REG", ["129.82.123.45", "5001", "1234abcd"]).decode("utf-8"))
    print(query_builder("REGOK", ["2", "129.82.123.45", "5001", "64.12.123.190", "34001"]).decode("utf-8"))
