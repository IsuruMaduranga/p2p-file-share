import os


def search_file(file_name: str):
    file_name = file_name.lower().split(" ")
    file_found = False
    file_names = []

    if os.path.exists("data"):
        available_files = os.listdir("data")
        for file in available_files:
            file_tokens = file.lower().split(" ")
            print(file_tokens)
            for token in file_name:
                if token not in file_tokens:
                    break
            else:
                file_found = True
                file_names.append(file)

    return file_found, " ".join(file_names)


def process_request(request_tokens):
    processed_request = {}
    if request_tokens[1] == "JOIN":
        processed_request['request'] = "JOIN"
        return processed_request

    elif request_tokens[1] == "LEAVE":
        processed_request['request'] = "LEAVE"
        return processed_request

    elif request_tokens[1] == "SER":
        processed_request['request'] = "SER"
        hop_count = int(request_tokens[5]) - 1

        file_found, file_names = search_file(request_tokens[4])
        processed_request['file_found'] = file_found

        if file_found:
            processed_request['file_names'] = file_names

        processed_request['hop_count'] = hop_count
