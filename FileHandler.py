import os
import random
from utils import query_builder,udp_send_recv,pretty_print_message_to_cli
import requests
import configuration as cfg
from tqdm import tqdm
from exceptions import ResourceNotFoundError

def show_files():
    file_names = []
    dir = cfg.Application['dir']
    if os.path.exists(dir):
        available_files = os.listdir(dir)
        for file in available_files:
            file_names.append(file)
    return file_names

def downloadFile(filename, ip, port):
    filename = filename.replace(" ","-")
    url = 'http://' + ip + ":" + port + "/" + filename
    try:
        r = requests.get(url, allow_redirects=True, stream=True)
        if r.status_code == 404:
            raise ResourceNotFoundError
        total = int(r.headers.get('content-length', 0))
        fname = filename.replace("-"," ")
        fname = f"{cfg.Application['dir']}/{fname}"
        with open(fname, 'wb') as file, tqdm(desc=fname, total=total, unit='iB', unit_scale=True,unit_divisor=1024,) as bar:
            for data in r.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
        pretty_print_message_to_cli(" Successfully Downloaed File : " + filename)
    except:
        pretty_print_message_to_cli("The Requested Resource Does Not Exist")

def search_file(filename, local_search = False):
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
            pretty_print_message_to_cli("File Found in the Local Repository")
        else:
            ip = cfg.UdpServer['ip']
            port = cfg.UdpServer['port']
            request = query_builder("SER", [ip,port, filename, 3])  #NO of HOPS = 3
            return udp_send_recv(ip, port, request, recieve=False)
    else:
        return file_found, " , ".join(file_names)    
