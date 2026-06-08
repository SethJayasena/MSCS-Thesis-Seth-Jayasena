#the receiver / client receives the binary map from the sender / server

import socket 
import struct 
import numpy as np 
import matplotlib.pyplot as plt 

def main():

    #client socket 
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #server and client are on the same laptop currently, so use
    #localhost
    ipAddress = "127.0.0.1"
    port = 8000

    clientSocket.bind((ipAddress, port))
    #configure the bound socket to accept incoming connection requests 
    clientSocket.listen(1)

    #block to wait for an incoming client connection on the port 
    connection, address = clientSocket.accept() 

    #receive the header
    numHeaderBytes = 12
    header = connection.recv(numHeaderBytes) 

    #unpack the header 
    #"!III" means:
    #network byte order (big-endian)
    #3 unsigned 32-bit integers 
    height, width, payloadLength = struct.unpack(
        "!III",
        header 
    )

    #for the payload, initialize it with an empty byte literal 
    payload = b"" 

    while len(payload) < payloadLength: 
        receiveSize = 4096

        #receive part of the payload 
        bytes = connection.recv(receiveSize)

        #didn't receive anything, so we can stop receiving the 
        #payload now
        if not bytes: 
            break 

        #append the bytes that we received to the payload 
        payload += bytes 

    #interpret the byte sequence as a 1D NumPy array 
    packed = np.frombuffer(payload, dtype = np.uint8)

    #unpack the bits 
    bits = np.unpackbits(packed) 

    #to construct the binary map, use the first n bits from "bits", where
    #n is height * width 
    binaryMap = bits[:height * width]
    #make sure that the dimensions of the binary map are correct 
    binaryMap = binaryMap.reshape(height, width) 

    print(binaryMap)

    connection.close() 
    clientSocket.close() 

    #render a 2D image of the binary map's data. 
    #Use "gray_r" for the colormap so that 0 will appear white, and 
    # 1 will appear black. 
    plt.imshow(binaryMap, cmap = "gray_r", vmin = 0, vmax = 1)
    plt.title("Binary Image") 
    plt.show() 


if __name__ == "__main__":
    main()