import socket
import sys
import os
import time

#server folder
servFolder = "./servData/"
#client folder
cliFolder = "./cliData/"
#list of commands for terminal
commands = ["get", "put", "ls", "quit"]
# 10 byte header size
header = 10

# keeps getting data until all of the bytes have been received
def getData(sock, size):
    #returns the size of in bytes
    return sock.recv(size).decode("utf-8")

# keeps sending data until all of the bytes have been sent
def sendData(sock, data):
    data = data.encode("utf-8")
    sentSize = 0
    while (len(data) > sentSize):
        sentSize += sock.send(data[sentSize:])

# get data from the specified server
def getServData(sock, file):
    # send the file we want to receive
    sentFile = file.encode()
    sock.send(sentFile)

    # receive the size of the file and convert to decimal
    acceptSize = sock.recv(40)
    acceptSize = acceptSize.decode()
    acceptSize = int(acceptSize)

    # make a temp. variable to hold the incoming data
    temp = ""
    while(True):
        text = sock.recv(40)
        temp += text.decode()
        if (len(temp) == acceptSize):
            sock.send("1".encode())
            print("THE FILE HAS BEEN ACCEPTED!")
            break

    # open a file path
    path = os.path.join(cliFolder, file)
    data = open(path, "w")
    # write file of recieved data
    data.write(temp)

    # print to notify the user file size and name
    print("The name of the file is: " + file)
    print("The size downloaded is: " + str(acceptSize) + " bytes")

    return 0

# send data from specified server
def sendServData(sock):
    file = sock.recv(40)
    file = file.decode()

    # find the file and then store the file
    path = os.path.join(servFolder, file)
    data = open(path)
    # read the contents of the file
    info = data.read()

    # save the size of the content and send it
    acceptLen = str(len(info)).encode()
    sock.send(acceptLen)
    
    # loops repeatedly until everything is sent
    while(True):
        info = info.encode()
        sock.send(info)
        acceptData = sock.recv(40)
        acceptData = acceptData.decode()
        if (acceptData == "1"):
            print("Your file has been sent successfully!")
            break
        # makes sure that content is sent in 0.5sec increments
        time.sleep(.500)
    return 0

# re-adjust the size of the data to make sure it fits the header
def dataSize(data, size):
    data = str(data)
    while (len(data) < size):
        data = "0" + data
    return data