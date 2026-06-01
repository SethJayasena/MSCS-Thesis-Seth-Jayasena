#Install and import the pertinent libraries
!pip3 install spectral numpy folium pandas
import spectral.io.envi as envi
from spectral import *
#import matplotlib
import matplotlib.pyplot as plt
%matplotlib inline
#import numpy
import numpy as np
import folium
import requests
from IPython.display import display
import math

#open the HSI file
fileHSI = envi.open("pic2.hdr", "pic2.hsi")

#load the entire data cube into a numpy array
#for processing 
dataCube = fileHSI.load() 

#run an algorithm to process the HSI file 

#reduce each HSI pixel to a binary 

#stream the binary data to another device 

#render the data as a straight line 


