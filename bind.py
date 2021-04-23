'''
Henry Torres
Armon Rahimi
Jared Schneider
Jonathan Story
'''
import socket

# connect the port and header
def connect(address, port):
    try:
        servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servSock.connect((address, port))
        print("Connected to " + address + " on port " + str(port))
    except Exception as exc:
        print(exc)
        return None
    return servSock


# bind the port
def bind(port = 0):
    try:
        servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servSock.bind(('', port))
        servSock.listen(1)
    except Exception as exc:
        print(exc)
        return None
    return servSock