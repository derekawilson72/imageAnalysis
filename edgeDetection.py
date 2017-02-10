
# coding: utf-8

## Edge Detection with skimage

# This tutorial illustrates edge detection with Python's skimage commands

### import packages

# In[9]:

get_ipython().magic(u'matplotlib inline')
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.image as img
from PIL import Image

from skimage.data import camera
from skimage.filter import roberts, sobel, scharr, prewitt, canny, gaussian_filter, edges
from numpy import array


# Load image data from files

# In[10]:

imName='images/7th49th/cctv4391.jpg'
image=Image.open(imName).convert("L")
image=array(image)


                Perform the edge detection algorithms
                
# In[11]:

edge_roberts = roberts(image)
edge_sobel = sobel(image)
edge_canny = canny(image,low_threshold=100, high_threshold=200)
edge_gaussian= gaussian_filter(image,1)
edge_prewitt = prewitt(image)


                Plot the results
                
# In[12]:

fig, ax = plt.subplots(ncols=3, nrows=2, sharex=True, sharey=True,
                       figsize=(10, 5))

ax[0,0].imshow(image, cmap=plt.cm.gray)
ax[0,0].set_title('Original Image')

ax[0,1].imshow(edge_sobel, cmap=plt.cm.gray)
ax[0,1].set_title('Sobel Edge Detection')

ax[0,2].imshow(edge_canny, cmap=plt.cm.gray)
ax[0,2].set_title('Canny Edge Detection')

ax[1,0].imshow(edge_gaussian, cmap=plt.cm.gray)
ax[1,0].set_title('Gaussian Edge Detection')

ax[1,1].imshow(edge_prewitt, cmap=plt.cm.gray)
ax[1,1].set_title('Prewitt Edge Detection')

ax[1,2].imshow(edge_roberts, cmap=plt.cm.gray)
ax[1,2].set_title('Roberts Edge Detection')

plt.show()
fig.canvas.draw()


# The above method shows sharp detection of pedestrians with all of the edge detection methods.  The optimum method is not clearly distinguishable.
