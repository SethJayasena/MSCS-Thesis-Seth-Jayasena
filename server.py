#Install and import the pertinent libraries
#!pip3 install spectral numpy folium pandas
import spectral.io.envi as envi
from spectral import *
#import matplotlib
import matplotlib.pyplot as plt
#%matplotlib inline
#import numpy
import numpy as np
import folium
import requests
from IPython.display import display
import math
import socket
import struct

#function to find the closest value to a target value in a list.
#Return the index of the closest value (indices are zero-indexed)
def findClosest(valList, target):

    return min( 
        range(len(valList)),
        #to find the closest value to the target, find the value with 
        #the smallest absolute difference between that value and the 
        #target
        key = lambda i: abs(float(valList[i]) - target)
    )

#SIMIS algorithm
def simisAlgorithm(cubeHSI, wavelengths):
    #load the entire data cube into a numpy array
    #for processing 
    #dataCube = fileHSI.load() 

    #run the SIMIS algorithm to process the HSI file 

    #calculate the channels that we should use in the SIMIS algorithm 

    '''
    In the original SIMIS algorithm, the following bands are used:
    620: absorption of phycocyanin
    709: not absorbed by phycocyanin
    665: absorbed by chlorophyll

    Our sensor does not necessarily have those exact bands, so we will 
    calculate which bands we should use instead 
    '''

    #find the closest bands to 620, 709, and 665
    corresponding620Band = findClosest(wavelengths, 620)
    corresponding709Band = findClosest(wavelengths, 709)
    corresponding665Band = findClosest(wavelengths, 665)

    #rho values (rho_w) for the bands closest to 620 and 709
    rho_w620 = cubeHSI[:, :, corresponding620Band]
    rho_w709 = cubeHSI[:, :, corresponding709Band]
    rho_w665 = cubeHSI[:, :, corresponding665Band]

    #absorption coefficients of water at the 620, 665, and 709 bands. 
    #These values come from the buiteveld et al 1994 table
    aw620 = 0.281
    aw665 = 0.3423
    aw709 = 0.6993

    #backscattering coefficient 
    backscatteringCoefficient = 1.61 * rho_w709 / (0.082 - 0.6 * rho_w709) 

    #conversion factor
    epsilon = 0.24

    gamma, delta = 1, 1

    #estimate chlorophyll-a presence 
    a_chl665 = ((rho_w709 / rho_w665) * (aw709 + backscatteringCoefficient - aw665)) / gamma

    #final result 
    simisResult = ((((rho_w709 / rho_w620) * (aw709 + backscatteringCoefficient)) - backscatteringCoefficient - aw620) /delta) - epsilon * a_chl665

    return simisResult

#function to stream the binary data to another device 
def streamData(binaryMap): 
    #currently, each bit occupies a full byte. So, we want to pack the 
    #bits. This will reduce the size by roughly 8x 
    packed = np.packbits(binaryMap)

    #the receiver should know the height and width of the map
    height, width = binaryMap.shape 

    #for the communication method, use TCP sockets. This file 
    #represents the server
    serverSocket = socket.socket() 

    #connect to the IP Address and port.
    #For now, we are testing on the same machine, so set the IP Address
    #to 127.0.0.1 (localhost)
    ipAddress = "127.0.0.1"
    port = 8000
    serverSocket.connect((ipAddress, port))

    #serialize the header 
    #"!III" means:
    #network byte order (big-endian)
    #3 unsigned 32-bit integers 
    header = struct.pack(
        "!III", 
        height, 
        width, 
        len(packed)
    )

    #send the header to the receiver
    serverSocket.sendall(header)

    #send the payload, which is the packed binary map 
    #convert to bytes 
    serverSocket.sendall(packed.tobytes())

    serverSocket.close()
    



def main():
    #open the HSI file
    #fileHSI = envi.open("HSI_Summer2025_Data/100_feet/100_2/100_2.hdr", "HSI_Summer2025_Data/100_feet/100_2/100_2.hsi")

    img = envi.open("../HSI_Summer2025_Data/100_feet/100_2/100_2.hdr", "../HSI_Summer2025_Data/100_feet/100_2/100_2.hsi")

    #cube representing the HSI data
    cubeHSI = np.array(img.load())

    #wavelengths from the sensor
    wavelengths = img.metadata["wavelength"]

    #run the SIMIS algorithm
    simisResult = simisAlgorithm(cubeHSI, wavelengths)


    #reduce each HSI pixel to a binary 

    #use the mean as a threshold for now 
    threshold = np.mean(simisResult) 
    binaryMap = simisResult > threshold

    #use 0s (false) and 1s (true)
    binaryMap = binaryMap.astype(np.uint8)

    #stream the binary data to another device 
    streamData(binaryMap)

if __name__ == "__main__":
    main()