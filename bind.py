import socket

#Connect to the port in the header
def connect(address, port):
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.connect((address, port))
        print("Connected to " + address + " on port " + str(port))
    except Exception as e:
        print(e)
        return None
    return serverSocket


#Bind the port, listen for incoming connections
def bind(port = 0):
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind(('', port))
        serverSocket.listen(1)
    except Exception as e:
        print(e)
        return None
    return serverSocket