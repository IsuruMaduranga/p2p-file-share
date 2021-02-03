HEADER_LENGTH = 4
BUFFER_SIZE = 9999

RESPONSE_CODES = {
    "REGOK" : {
        "0" : {"stat":True,"msg":"request is successful, no nodes in the system"},
        "1" : {"stat":True,"msg":"request is successful, 1 or 2 nodes' contacts will be returned"},
        "2" : {"stat":True,"msg":"request is successful, 1 or 2 nodes' contacts will be returned"},
        "9999" : {"stat":False,"msg":"failed, there is some error in the command"},
        "9998" : {"stat":False,"msg":"failed, already registered to you, unregister first"},
        "9997" : {"stat":False,"msg":"failed, registered to another user, try a different IP and port"},
        "9996" : {"stat":False,"msg":" failed, can’t register. BS full"}
    },
    "UNREG" : {}
}