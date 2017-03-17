
from numpy import linspace, sin
from matplotlib.pyplot import  imread, get_cmap

from chaco.api import ArrayPlotData, HPlotContainer, Plot
from chaco.tools.api import PanTool, ZoomTool
from enable.component_editor import ComponentEditor
from traits.api import HasTraits, Instance, Property, Int, Float, Array, on_trait_change, Instance, DelegatesTo
from traitsui.api import Item, View, RangeEditor
from chaco.api import ImageData, ImagePlot
from chaco.default_colormaps import  gray

from imageModel import imageModel

class ConnectedRange(HasTraits):

    model = Instance(imageModel)

    
    upper = DelegatesTo('model')
    lower = DelegatesTo('model')
    c     = DelegatesTo('model')
    lowerLimit= DelegatesTo('model')
    upperLimit= DelegatesTo('model')


    
    img       = DelegatesTo('model')
    hist      = DelegatesTo('model')
    lowerFilt = DelegatesTo('model')
    upperFilt = DelegatesTo('model')
    edges     = DelegatesTo('model')
    fill      = DelegatesTo('model')
    elevation = DelegatesTo('model')
    markers   = DelegatesTo('model')
    segmentation = DelegatesTo('model')

    container01 = Instance(HPlotContainer)
    container02 = Instance(HPlotContainer)
    
    imgdata = Instance(ArrayPlotData)
    upfilt  = Instance(ArrayPlotData)
    lowfilt = Instance(ArrayPlotData)
    edgesPlot= Instance(ArrayPlotData)
    fillPlot = Instance(ArrayPlotData)
    elevPlot = Instance(ArrayPlotData)
    markerPlot= Instance(ArrayPlotData)
    segmentationPlot = Instance(ArrayPlotData)

    traits_view = View(Item('container01', 
                            editor=ComponentEditor(), 
                            show_label=False),
                       Item('container02', 
                            editor=ComponentEditor(), 
                            show_label=False),
                       Item('upper', editor=RangeEditor(low=0., high=240.), label="upperbound"),
                       Item('lower', editor=RangeEditor(low=0., high=240.), label="lowerbound"),
                       Item('lowerLimit', editor=RangeEditor(low=0., high=256.), label="lowerLimit"),
                       Item('upperLimit', editor=RangeEditor(low=0., high=256.), label="upperLimit"),
                       
                       
                       Item('c', editor=RangeEditor(low=-5., high=5.)),
                       resizable=True,
                       title="Connected Range")
    
   

    def _imgdata_default(self):
        img=self.img
        imgdata = ArrayPlotData(imagedata = img, colormap=gray)
        return imgdata

    def _upfilt_default(self):
        img=self.upperFilt
        imgdata = ArrayPlotData(imagedata = img, colormap=gray)
        return imgdata

    def _lowfilt_default(self):
        img=self.lowerFilt
        imgdata = ArrayPlotData(imagedata = img, colormap=gray)
        return imgdata
    
    def _edgesPlot_default(self):
        edges=self.edges
        imgdata = ArrayPlotData(imagedata = edges, colormap=gray)
        return imgdata

    def _fillPlot_default(self):
        fill=self.fill
        imgdata = ArrayPlotData(imagedata = fill, colormap=gray)
        return imgdata

    def _elevPlot_default(self):
        elev=self.elevation
        imgdata = ArrayPlotData(imagedata = elev)
        return imgdata

    def _markerPlot_default(self):
        markers=self.markers
        imgdata = ArrayPlotData(imagedata = markers)
        return imgdata

    def _segmentationPlot_default(self):
        segmentation=self.segmentation
        imgdata = ArrayPlotData(imagedata = segmentation)
        return imgdata

    def _container02_default(self):
        # Create the data and the PlotData object
        fillPlot=self.fillPlot
        fill = Plot(fillPlot)
        fill.img_plot("imagedata", colormap=gray)

        elev = Plot(self.elevPlot)
        elev.img_plot("imagedata", colormap=gray)
        
        marker = Plot(self.markerPlot)
        marker.img_plot("imagedata", colormap=gray)

        segmentation = Plot(self.segmentationPlot)
        segmentation.img_plot("imagedata", colormap=gray)

        return HPlotContainer(fill, elev, marker, segmentation)

    def _container01_default(self):
        # Create the data and the PlotData object

        
        imgdata    = self.imgdata
        upperfilter= self.upfilt
        lowerfilter= self.lowfilt
        edgesPlot  = self.edgesPlot
        # Create the scatter plot
        scatter = Plot(imgdata)
        scatter.img_plot("imagedata", colormap=gray)
        
        # Create the line plot
        line = Plot(upperfilter)
        line.img_plot("imagedata", colormap=gray)


        # Create the other line plot
        line2 = Plot(lowerfilter)
        line2.img_plot("imagedata", colormap=gray)

        
        #create edges
        edgeplot = Plot(edgesPlot)
        edgeplot.img_plot("imagedata", colormap=gray)


       # Add pan/zoom so we can see they are connected
        scatter.tools.append(PanTool(scatter))
        scatter.tools.append(ZoomTool(scatter))
        line.tools.append(PanTool(line))
        line.tools.append(ZoomTool(line))
        line2.tools.append(PanTool(line))
        line2.tools.append(ZoomTool(line))
        
        
        # Set the two plots' ranges to be the same
        #scatter.index_range = line.index_range
        #scatter.value_range = line.value_range
        ##set manually with scatter.value_range.set_bounds(0,1)
        ##or scatter.index_range.set_bounds(0,1)


        # Create a horizontal container and put the two plots inside it
        return HPlotContainer(scatter, line, line2, edgeplot)
    
    @on_trait_change('img')
    def update_img(self):
        self.imgdata.set_data('imagedata', self.img)
    
    @on_trait_change('upperFilt')
    def update_upperFilter(self):
        self.upfilt.set_data('imagedata', self.upperFilt)

    @on_trait_change('lowerFilt')
    def update_lowerFilter(self):
        self.lowfilt.set_data('imagedata', self.lowerFilt)

    @on_trait_change('edges')
    def update_edges(self):
        self.edgesPlot.set_data('imagedata', self.edges)

    @on_trait_change('fill')
    def update_fill(self):
        self.fillPlot.set_data('imagedata', self.fill)

    @on_trait_change('elevation')
    def update_elevation(self):
        self.elevPlot.set_data('imagedata', self.elevation)

    @on_trait_change('markers')
    def update_markers(self):
        self.markerPlot.set_data('imagedata', self.markers)

    @on_trait_change('segmentation')
    def update_segmentation(self):
        self.segmentationPlot.set_data('imagedata', self.segmentation)


if __name__ == "__main__":

    im1 = imageModel()
    demo=ConnectedRange(model=im1)
    demo.edit_traits() #demo.configure_traits()
    
