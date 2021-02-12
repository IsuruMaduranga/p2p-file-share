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

        file_found = False
        file_names = " "
        ''' TODO
        Search for the file
        '''
        processed_request['file_found'] = file_found

        if file_found:
            processed_request['file_names'] = file_names

        processed_request['hop_count'] = hop_count
