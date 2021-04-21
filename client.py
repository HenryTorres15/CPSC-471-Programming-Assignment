import os, sys, socket
from dataLink import getData, sendData, getServData, dataSize

# server folder
servFolder = "./servData/"
# client folder
cliFolder = "./cliData/"
# list of commands for terminal
commands = ["get", "put", "ls", "quit"]
# 10 byte header size
header = 10

# connect the port and header
def connect(loc, port):
    try:
        servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servSock.connect((loc, port))
        print("Actively connected to " + loc + " and is on port " + str(port))
    except Exception as exc:
        print(exc)
        return None
    return servSock

# client side put file
def putFile(sock, loc, fileName):
    # create variable for files in client folder
    path = cliFolder + fileName

    # retrieve the size and open the file
    try:
        user = open(path, "r")
        fileLength = os.path.getsize(path)
    except Exception as exc:
        print(exc)
        return

    # port number from server
    channelPort = getData(sock, header)

    # create a new connection to a new port
    dataSock = connect(loc, int(channelPort))

    # error message for a failed connection
    if (not dataSock):
        print("Error, the connection to server has failed.")
        return
    
    # the size of the fileName
    nameSize = dataSize(len(fileName), header)
    # the size of the file
    file_dataSize = dataSize(fileLength, header)
    # read what's inside the file
    fileData = user.read()
    
    # create a payload
    data = nameSize + file_dataSize + fileName + fileData

    # send data from socket and print messages that it was recieved.
    sendData(dataSock, data)
    print(fileName + " file has been uploaded successfully.")
    print("The uploaded size is " + str(len(data)) + " bytes.")

    # close file
    user.close()
    # close connection
    dataSock.close()
    print("The data transfer connection has been closed.")


def main(argu):
    # make sure user writes the correct command for client.py
    if (len(argu) != 3):
        print("Please use python3 " + argu[0] + " <SERVER> <PORT>")
        sys.exit()

    server = argu[1]
    port = argu[2]

    # trying to connect to server
    cliSocket = connect(server, int(port))
    if (not cliSocket):
        # print a messgae if it does not connect
        print("Error, failed to connect to " + server)
        sys.exit()

    ask = ""
    
    # stays on until the user decides to terminate or quit
    while True:
        ask = (input("ftp> ")).lower().split()

        # get <FILE NAME> which downloads the file from the server
        if (ask[0] == commands[0]):
            if (len(ask) != 2):
                print("Please use: get <FILE NAME> (downloads file from the server)")
            else:
                sendData(cliSocket, ask[0])
                getServData(cliSocket, ask[1])
            
        # put <FILE NAME> which upoads the file from the server
        elif (ask[0] == commands[1]):
            if (len(ask) != 2):
                print("Please use: put <FILE NAME> (uploads file to the server)")
            else:
                sendData(cliSocket, ask[0])
                putFile(cliSocket, server, ask[1])
            
        # ls - returns a list of all the files in the given directory
        elif (ask[0] == commands[2]):
            # send data from socket
            sendData(cliSocket, ask[0])

            # variable for the size of repsonse
            respSize = getData(cliSocket, header)

            if (respSize == ""):
                print("Error, the size of the response was not received.")
            else:
                response = getData(cliSocket, int(respSize))
                print(response)

        # quit - disconnects from the server and exits
        elif (ask[0] == commands[3]):
            sendData(cliSocket, ask[0])
            cliSocket.close()
            print("The client connection is now closed.")
            break
        
        else:
            print("Command does not exist.")
            # giving user examples for which commands to use
            print("Please use one of the following: get <fileName>, put <fileName>, ls, quit")


if __name__ == '__main__':
    main(sys.argv)