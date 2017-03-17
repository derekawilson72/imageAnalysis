from numpy import  linspace, array, zeros, size
from traits.api import HasTraits, Float, Int,  Array, Property, Range
from numpy import linspace, sin
from matplotlib.pyplot import  imread

from imageSegmentationFunctions import makeImg, makeHist, lowerFilterHist, upperFilterHist, makeEdges, makeFill, makeClean, makeElevation, makeMarkers, makeSegmentation, segmentationDifference, calcObjects

class imageModel(HasTraits):

    imName= 'cctv4390.jpg'
    imDir = 'images/7th49th/'
    upper = Float(79.8)
    lower = Float(18.568)
    c = Float(4.0)

    lowerLimit=Float(116.30)
    upperLimit=Float(112.26)
    
    img  =  Property(depends_on=['upper', 'lower', 'c']) 
    hist =  Property(depends_on=['upper', 'lower', 'c']) 
    lowerFilt =  Property(depends_on=['upper', 'lower', 'c',  'lowerLimit', 'upperLimit']) 
    upperFilt =  Property(depends_on=['upper', 'lower', 'c',  'lowerLimit', 'upperLimit']) 
    edges     =  Property(depends_on=['upper', 'lower', 'c']) 
    fill      =  Property(depends_on=['upper', 'lower', 'c']) 
    elevation =  Property(depends_on=['upper', 'lower', 'c']) 
    markers   =  Property(depends_on=['upper', 'lower', 'c',  'lowerLimit', 'upperLimit']) 
    segmentation = Property(depends_on=['upper', 'lower', 'c',  'lowerLimit', 'upperLimit']) 


    def _upper_changed(self, old, new):
        
        #print 'upper changed to ', new
        pass
    
    def _get_segmentation(self):
        elevation_map = self.elevation
        markers       = self.markers
        segmentation = makeSegmentation(elevation_map, markers)
        return segmentation

    def _segmentation_default(self):
        elevation_map = self.elevation
        markers       = self.markers
        segmentation = makeSegmentation(elevation_map, markers)
        return segmentation
    

    def _get_markers(self):
        markers=makeMarkers(self.img, self.lowerLimit, self.upperLimit)
        return markers

    def _markers_default(self):
        markers=makeMarkers(self.img, self.lowerLimit, self.upperLimit)
        return markers

    
    def _get_elevation(self):
        elevation= makeElevation(self.img)
        return elevation

    def _elevation_default(self):
        elevation= makeElevation(self.img)
        return elevation


    def _get_fill(self):
        fill= makeFill(self.edges )
        return fill

    def _fill_default(self):
        fill= makeFill(self.edges)
        return fill


    def _get_edges(self):
        edges= makeEdges(self.img )
        return edges

    def _edges_default(self):
        edges= makeEdges(self.img )
        return edges


    def _get_img(self):
        lower=int(round(self.lower))
        upper=int(round(self.upper))
        imageFile= self.imDir +  self.imName 
        img=makeImg(imageFile, upper, lower, plot=False)
        return img

    def _img_default(self):
        imageFile= self.imDir +  self.imName 
        img=makeImg(imageFile, plot=False)
        return img


    def _get_hist(self):
        hist=makeHist(self.img)
        return hist

    def _get_lowerFilt(self):
        filt=lowerFilterHist(self.img, lowerLimit=self.lowerLimit, upperLimit=self.upperLimit)
        return filt

    def _get_upperFilt(self):
        filt=upperFilterHist(self.img, lowerLimit=self.lowerLimit, upperLimit=self.upperLimit)
        return filt


    def _get_edges(self):
        edges= makeEdges(self.img )
        return edges

    def _edges_default(self):
        edges= makeEdges(self.img )
        return edges
