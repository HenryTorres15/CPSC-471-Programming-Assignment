'''
Henry Torres
Armon Rahimi
Jared Schneider
Jonathan Story
'''
import os
import sys
import socket
from dataLink import getData, sendData, sendServData, dataSize


#server folder
servFolder = "./servData/"
#client folder
cliFolder = "./cliData/"
#list of commands for terminal
commands = ["get", "put", "ls", "quit"]
# 10 byte header size
header = 10

# bind function 
def bind(port = 0):
    try:
        # bind the socket to the port
        servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servSock.bind(('', port))
        servSock.listen(1)
    except Exception as i:
        print(i)
        return None
    # return the server socket 
    return servSock

# server side get file
def getFile(sock):
    # make a new sock with respect to bind()
    newSock = bind()

    # send port to client 
    servPort = newSock.getsockname()[1]
    sendData(sock, str(servPort))

    # print an acception message
    print("Listening on specific port: " + str(servPort))
    sockData, loc = newSock.accept()
    print("Actively connected to: " + loc[0])

    # get the sizes of the file message and file size
    fileMessSize = getData(sockData, header)
    fileSize = getData(sockData, header)

    # checking is file message is empty
    if (fileMessSize == ""):
        print("Error failed to accept the file name size.")
        return
    # checking if file size is empty
    if (fileSize == ""):
        print("Error failed to accept the data size.")
        return

    # create variables and retreieve size
    name = getData(sockData, int(fileMessSize))
    data = getData(sockData, int(fileSize))

    # create a path
    path = servFolder + name
    # open the path
    user = open(path, "w")
    # write on the file
    user.write(data)

    # printing a message if the file and file size has been received
    print(name + " has been received!")
    print("The transferred size is : " + fileSize + " bytes.")

    # close the file
    user.close()
    # close the connection
    sockData.close()
    print("File and data socket are now closed.")

def main(argu):
    # make sure the user writes the correct command on terminal to run server.py
    if (len(argu) != 2):
        print("Please use py " + argu[0] + " <PORT>")
        sys.exit()

    port = argu[1]

    # bind the socket to port 
    servSock = bind(int(port))
    if (not servSock):
        print("Error port is not able to be binded.")
        sys.exit()

    # keeps listening until user terminates the program
    while (True):
        print("Actively listening to " + port)
        cliSock, loc = servSock.accept()
        print("Actively connected to " + loc[0])

        # loops for terminal commands on ftp
        while (True):
			# get the info that is being passed from in from the client
            ask = getData(cliSock, header)

            # get the file name and download the file name from the server
            if (ask == commands[0]):
                sendServData(cliSock)

            # put the file name and upload it the client
            elif (ask == commands[1]):
                getFile(cliSock)

            # the ls command will create a list of items in that directory
            elif (ask == commands[2]):
                # get all items from the folder
                files = os.listdir(servFolder) 
                # keeps the repsonse active
                resp = "" 
                for file in files:
                    resp += file + "  "
                resp = resp[:-2]

                # this send the repsonse
                respSize = dataSize(len(resp), header)
                data = respSize + resp
                sendData(cliSock, data)

            # closes the connection by typing quit in terminal
            elif (ask == commands[3]):
                cliSock.close()
                print("The server connection is now closing.")
                break
            # otherwise is closes the connection
            else:
                print("Command does not exist, closing the connection.")
                cliSock.close()
                break

if __name__ == '__main__':
    main(sys.argv)