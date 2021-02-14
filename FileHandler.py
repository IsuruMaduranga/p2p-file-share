import os
import random
from utils import query_builder,udp_send_recv

def show_files(base):
    file_names = []
    if os.path.exists(base):
        available_files = os.listdir(base)
        for file in available_files:
            file_names.append(file)
    return file_names

def search_file(base, file_name):
    file_name = file_name.lower().split(" ")
    file_found = False
    file_names = []

    if os.path.exists(base):
        available_files = os.listdir(base)
        for file in available_files:
            file_tokens = file.lower().split(" ")

            for token in file_name:
                if token not in file_tokens:
                    break
            else:
                file_found = True
                file_names.append(file)

    return file_found, " ".join(file_names)
    
def search_file_remote(ip, port, filename):
    request = query_builder("SER", [ip, port, filename, 3])  #NO of HOPS = 3
    udp_send_recv(ip, port, request, recieve=False)




