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


def main():
    #open the HSI file
    #fileHSI = envi.open("HSI_Summer2025_Data/100_feet/100_2/100_2.hdr", "HSI_Summer2025_Data/100_feet/100_2/100_2.hsi")

    img = envi.open("../HSI_Summer2025_Data/100_feet/100_2/100_2.hdr", "../HSI_Summer2025_Data/100_feet/100_2/100_2.hsi")

    #cube representing the HSI data
    cubeHSI = np.array(img.load())

    #wavelengths from the sensor
    wavelengths = img.metadata["wavelength"]

    print("wavelengths:")
    print(wavelengths)

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

    #rho values for the bands closest to 620 and 709
    rho620 = cubeHSI[:, :, corresponding620Band]
    rho709 = cubeHSI[:, :, corresponding709Band]

    #ratio between the water-leaving reflectance of the 
    #709 and 620 bands 

    ratio709And620Bands = rho709 / rho620

    print(ratio709And620Bands)

    #find the absorption coefficient of water at the 709 band + a
    #backscattering coefficient 

    #find the absorption coefficient of water at the 620 band 

    

    #reduce each HSI pixel to a binary 

    #stream the binary data to another device 

    #render the data as a straight line 


if __name__ == "__main__":
    main()