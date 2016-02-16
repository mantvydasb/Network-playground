import socket
import threading
import sys

LOCAL_HOST = "192.168.2.2"
LOCAL_PORT = 8080
# LOCAL_ADDRESS = "127.0.0.1", 5555

def initVariables():
    arguments = sys.argv[1:]
    argumentsCount = len(arguments)

    if argumentsCount != 5:
        print("Usage: [localHost] [localPort] [remoteHost] [remotePort] [receiveFirst]")
    else:
        localHost = sys.argv[1]
        localPort = sys.argv[2]
        remoteHost = sys.argv[3]
        remotePort = sys.argv[4]
        shouldReceiveFirst = sys.argv[5]
        return localHost, localPort, remoteHost, remotePort, shouldReceiveFirst

def startListening(localHost, localPort, remoteHost, remotePort, shouldReceiveFirst):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((localHost, int(localPort)))
    server.listen(5)
    print ("# Simulating proxy server on: " + localHost + " " + str(localPort))

    # while True:

    # client socket - socket from a firefox web request with proxy pointing to 192.168.2.2 5555, hence we're picking up the connection request;
    # l_addres - proxy server address, r_address - client, which connected to our proxy, address;
    clientSocket, address = server.accept()
    print("Incoming connection from client: " + str(address))
    proxyThread = threading.Thread(target=distributeTraffic, args=(clientSocket, localHost, localPort, remoteHost, remotePort, shouldReceiveFirst))
    proxyThread.start()

def receiveFrom(socket):
    buffer = b''
    socket.settimeout(2)

    while True:
        data = socket.recv(4096)
        if not data: break
        else: buffer += data
    return buffer

def distributeTraffic(clientSocket, localHost, localPort, remoteHost, remotePort, shouldReceiveFirst):
    remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remoteSocket.connect((remoteHost, int(remotePort)))

    while True:
        # local data going through proxy to remote socket
        localBuffer = receiveFrom(clientSocket)
        localBufferLength = len(localBuffer)

        if len(localBuffer):
            print("Received %d bytes from localhost" % localBufferLength)
            hexdump(localBuffer)
            localBuffer = modifyLocalBuffer(localBuffer)
            remoteSocket.send(localBuffer)
            print("Sent to remote")

        # remote data going through proxy to local socket
        remoteBuffer = receiveFrom(remoteSocket)
        remoteBufferLength = len(remoteBuffer)

        if remoteBufferLength:
            print("Received %d bytes from remote" % remoteBufferLength)
            hexdump(remoteBuffer)
            remoteBuffer = modifyRemoteBuffer(remoteBuffer)
            clientSocket.send(remoteBuffer)
            print("Send to localhost")

def modifyRemoteBuffer(remoteBuffer):
    print("Buffer destined to remote host " + "got modified.")
    return remoteBuffer + " modified".encode("utf8")

def modifyLocalBuffer(localBuffer):
    print("Buffer destined to local host" + "got modified.")
    return localBuffer

def hexdump(source, length=16):
    print("Dumping HEX for remote buffer")
    print(source)

def main():
    # localHost, localPort, remoteHost, remotePort, shouldReceiveFirst = initVariables()

    localHost = LOCAL_HOST
    localPort = LOCAL_PORT
    remoteHost = "192.168.2.2"
    remotePort = 8506
    shouldReceiveFirst = False
    startListening(localHost, localPort, remoteHost, remotePort, shouldReceiveFirst)

main()