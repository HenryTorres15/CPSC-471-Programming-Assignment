import socket, sys, os, time
from dataLink import getData, sendData, getServData, dataSize

# 10 byte header size
header = 10
#server folder
servFolder = "./servData/"
#client folder
cliFolder = "./cliData/"
#list of commands for terminal
commands = ["get", "put", "ls", "quit"]

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

def put_file(sock, address, fileName):
    # grab files only from client folder
    filePath = cliFolder + fileName

    # open file and get file size
    try:
        userFile = open(filePath, "r")
        fileSize = os.path.getsize(filePath)
    except Exception as e:
        print(e)
        # print("Failed to open file")
        return

    # get data channel port number from server
    dataPort = getData(sock, header)

    # connect to new port
    dataSocket = connect(address, int(dataPort))

    # if connection failed, exit
    if not dataSocket:
        print("Failed to connect to server")
        return
    
    # make file size and file name headers
    fileNameSize = dataSize(len(fileName), header)
    fileDataSize = dataSize(fileSize, header)
    fileData = userFile.read()
    
    # add headers to payload
    data = fileNameSize + fileDataSize + fileName + fileData

    # send data
    sendData(dataSocket, data)
    print(fileName + " upload successful.")
    print("Bytes sent: " + str(len(data)))

    # close file and connection
    userFile.close()
    dataSocket.close()
    print("Data transfer connection closed")


def run(args):
    # To run: python3 cli.py <SERVER> <PORT>
    if len(args) != 3:
        print("Usage: python3 " + args[0] + " <SERVER> <PORT>")
        sys.exit()

    server = args[1]
    port = args[2]

    # connect to server
    cliSocket = connect(server, int(port))
    if not cliSocket:
        print("Failed to connect to " + server)
        sys.exit()

    query = ""

    while True:
        query = (input("ftp> ")).lower().split()
        # print(query)

        # get <FILE NAME>
        # downloads <FILE NAME> from the server
        if query[0] == commands[0]:
            if len(query) != 2:
                print("Usage: get <FILE NAME>")
            else:
                sendData(cliSocket, query[0])
                getServData(cliSocket, query[1])
            
        # put <FILE NAME>
        # uploads <FILE NAME> to the server
        elif query[0] == commands[1]:
            if len(query) != 2:
                print("Usage: put <FILE NAME>")
            else:
                sendData(cliSocket, query[0])
                put_file(cliSocket, server, query[1])
            
        # ls
        # lists files on the server
        elif query[0] == commands[2]:
            # send query
            sendData(cliSocket, query[0])

            # get size of response
            responseSize = getData(cliSocket, header)

            if responseSize == "":
                print("Failed to receive size of response")
            else:
                response = getData(cliSocket, int(responseSize))
                print(response)

        # quit
        # disconnects from the server and exits
        elif query[0] == commands[3]:
            sendData(cliSocket, query[0])
            cliSocket.close()
            print("Connection closed")
            break
        
        else:
            print("Invalid command")


if __name__ == '__main__':
    run(sys.argv)