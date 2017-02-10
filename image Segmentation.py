
# coding: utf-8

# In[1]:

get_ipython().magic(u'matplotlib inline')
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


# In[2]:

class imageMorph():
    
    imName='images/7th49th/cctv4390.jpg'
    topBoundary=160
    fig    =None
    axs    =None
    image  =None
    hist   =None
    edges  =None
    fill_coins=None
    elevation_map=None

    def __init__(self, imName='images/7th49th/cctv4390.jpg'):
        img=imread(imName)
        img=img[160:,: , :]
        image=io.imread(imName, as_grey=True)
        image=Image.open(imName).convert("L")
        image=array(image)
        image=image[160:,:]
        self.image=image
    
        fig, axs = plt.subplots(2, 5) #, figsize=(8, 3))
        self.fig=fig
        self.axs=axs

        self.makeHist()
        self.filterHist()
        self.makeEdges()
        self.makeFill()
        self.makeClean()
        self.makeElevation()
        self.makeMarkers()
        self.makeSegmentation()
        self.calcObjects()


    def makeHist(self):

        #coins = data.coins()
        image=self.image
        hist = np.histogram(image, bins=np.arange(0, 256))
        self.hist=hist
        ax1=self.axs[0,0]
        ax2=self.axs[0,1]
        ax1.imshow(image, cmap=plt.cm.gray, interpolation='nearest')
        ax1.axis('off')
        ax2.plot(hist[1][:-1], hist[0], lw=2)
        ax2.set_title('histogram of grey values')


    def filterHist(self):
        ax1=self.axs[0,2]
        ax2=self.axs[0,3]
        image=self.image
        ax1.imshow(image > 100, cmap=plt.cm.gray, interpolation='nearest')
        ax1.set_title('coins > 100')
        ax1.axis('off')
        ax1.set_adjustable('box-forced')
        ax2.imshow(image > 150, cmap=plt.cm.gray, interpolation='nearest')
        ax2.set_title('coins > 150')
        ax2.axis('off')
        ax2.set_adjustable('box-forced')
        margins = dict(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0, right=1)
        #fig.canvas.draw()
        # fig.subplots_adjust(**margins)


    def makeEdges(self):
        image=self.image
        edges = canny(image/255.)
        ax=self.axs[0,4]
        ax.imshow(edges, cmap=plt.cm.gray, interpolation='nearest')
        ax.axis('off')
        ax.set_title('Canny detector')
        self.edges=edges #fig.canvas.show()

    def makeFill(self):
        edges=self.edges
        fill_coins = ndi.binary_fill_holes(edges)
        ax=self.axs[1,0]
        ax.imshow(fill_coins, cmap=plt.cm.gray, interpolation='nearest')
        ax.axis('off')
        ax.set_title('Filling the holes')
        self.fill_coins=fill_coins

    def makeClean(self):
        fill_coins=self.fill_coins
        coins_cleaned = morphology.remove_small_objects(fill_coins, 21)
        ax=self.axs[1,1]
        ax.imshow(coins_cleaned, cmap=plt.cm.gray, interpolation='nearest')
        ax.axis('off')
        ax.set_title('Removing small objects')
        self.coins_cleaned=coins_cleaned


    def makeElevation(self):
        image=self.image
        elevation_map = sobel(image)
        ax=self.axs[1,2]
        ax.imshow(elevation_map, cmap=plt.cm.jet, interpolation='nearest')
        ax.axis('off')
        ax.set_title('elevation_map')
        self.elevation_map=elevation_map
        

    def makeMarkers(self):
        image=self.image
        markers = np.zeros_like(image)
        markers[image < 30] = 1
        markers[image > 150] = 2
        ax=self.axs[1,3]
        ax.imshow(markers, cmap=plt.cm.spectral, interpolation='nearest')
        ax.axis('off')
        ax.set_title('markers')
        self.markers=markers

    def makeSegmentation(self):
        elevation_map=self.elevation_map
        markers=self.markers
        segmentation = morphology.watershed(elevation_map, markers)
        ax=self.axs[1,4]
        ax.imshow(segmentation, cmap=plt.cm.gray, interpolation='nearest')
        ax.axis('off')
        ax.set_title('segmentation')
        self.segmentation =segmentation 


    def calcObjects(self):
        segmentation=self.segmentation
        local_maxi = peak_local_max(segmentation ,  indices=False, footprint=np.ones((3, 3)))
        markers = label(local_maxi)
        labeled, nr_objects = ndimage.label(local_maxi) #
        return nr_objects


# In[3]:

im1=imageMorph()

im2=imageMorph('images/7th49th/cctv4391.jpg')


# In[4]:

segdiff=im1.segmentation - im2.segmentation
fig,axs= plt.subplots(1, 3)
ax1=axs[0]
ax1.imshow(im1.segmentation, cmap=plt.cm.spectral, interpolation='nearest')

seg2=morphology.watershed(im2.elevation_map  , im1.markers)
ax2=axs[1]
ax2.imshow (seg2, cmap=plt.cm.spectral, interpolation='nearest')

seg2=array(seg2, dtype='f')
seg1=array(im1.segmentation , dtype='f')
seg3=seg2-seg1
seg3[seg3<0]=0
intseg3=array(seg3,dtype='uint8')

ax3=axs[2]
ax3.imshow(intseg3, cmap=plt.cm.spectral, interpolation='nearest')

objs=morphology.remove_small_objects(intseg3, 8, connectivity=2)
ax3.imshow(objs, cmap=plt.cm.spectral, interpolation='nearest')



# In[5]:

fig2,axs2= plt.subplots(1, 1)
axs2.imshow(objs, cmap=plt.cm.spectral, interpolation='nearest')
fig2.canvas.draw()


# In[ ]:



