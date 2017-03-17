
# coding: utf-8

# In[1]:

#get_ipython().magic(u'matplotlib inline')
import numpy as np
import matplotlib.pyplot as plt
from skimage import data
from skimage.filter import canny
from scipy import ndimage as ndi
from skimage import morphology
from skimage.filter import sobel
from skimage.feature import peak_local_max
from skimage.measure import label
from scipy import ndimage
from skimage import io
from PIL import Image
from matplotlib.pyplot import  imread
from numpy import array


def makeImg(imName, upper=None, lower=None, plot=True):
    #img=imread(imName)
    # Convert the image
    pil_im = Image.open(imName).convert('L')
    img=array(pil_im)
    img=img[-1::-1,] ##not necessary  ##well maybe it is
    img=img[lower:upper,:]
    return img



def makeHist(img):
    # coins = data.coins()
    image=img
    hist = np.histogram(image, bins=np.arange(0, 256))
    return hist


def lowerFilterHist(image, lowerLimit=30, upperLimit=150):
    lowerImage = (image >= lowerLimit)*1  #return ones or zeros
    return lowerImage


def upperFilterHist(image, lowerLimit=30, upperLimit=150):
    upperImage = (image <= upperLimit) *1
    return upperImage



def makeEdges(image ):
        edges = canny(image/255.) *1
        return edges 

def makeFill(edges):
    fill_coins = ndi.binary_fill_holes(edges)
    return fill_coins


def makeClean(fill_coins):
    coins_cleaned = morphology.remove_small_objects(fill_coins, 21)
    return coins_cleaned 


def makeElevation(image):
    elevation_map = sobel(image)
    return elevation_map
        

def makeMarkers(image, lowerLimit=30, upperLimit=150):
    markers = np.zeros_like(image)
    markers[image < lowerLimit] = 1
    markers[image > upperLimit] = 2
    return markers

def makeSegmentation(elevation_map, markers):
    segmentation = morphology.watershed(elevation_map, markers)
    return segmentation


def segmentationDifference(seg1, seg2):
    segdiff=seg1 - seg2
    return segdiff


def calcObjects(segmentation):
    local_maxi = peak_local_max(segmentation ,  indices=False, footprint=np.ones((3, 3)))
    markers = label(local_maxi)
    labeled, nr_objects = ndimage.label(local_maxi) #
    return nr_objects




