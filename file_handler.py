import os
import requests
import configuration as cfg
from utils import query_builder, udp_send_recv


def show_files():
    file_names = []
    directory = cfg.Application['dir']
    if os.path.exists(directory):
        available_files = os.listdir(directory)
        for file in available_files:
            file_names.append(file)
    return file_names


def download_file(filename, ip, port):
    filename = filename.replace(" ", "-")
    url = 'http://' + ip + ":" + port + "/" + filename
    try:
        r = requests.get(url, allow_redirects=True)
        filename = filename.replace("-", " ")
        open(f"{cfg.Application['dir']}/{filename}", 'wb').write(r.content)
    except:
        print("The Resource Does Not Exists")


def search_file(filename, local_search=False):
    file_name = filename.lower().split(" ")
    file_found = False
    file_names = []
    dir = cfg.Application['dir']
    if os.path.exists(dir):
        available_files = os.listdir(dir)
        for file in available_files:
            file_tokens = file.lower().split(" ")

            for token in file_name:
                if token not in file_tokens:
                    break
            else:
                file_found = True
                file_names.append(file)

    if local_search:
        if file_found:
            print("File Found in the Local Repository")
        else:
            ip = cfg.UdpServer['ip']
            port = cfg.UdpServer['port']
            request = query_builder("SER", [ip, port, filename, 3])  # NO of HOPS = 3
            udp_send_recv(ip, port, request, recieve=False)
    else:
        return file_found, " , ".join(file_names)
