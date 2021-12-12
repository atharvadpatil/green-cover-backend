from django.shortcuts import render

# generic base view
from django.views.generic import TemplateView 

#gee
import ee
ee.Initialize()


#folium
import folium
from folium import plugins

#geemap
# import geemap
import geemap.foliumap as geemap

#home
class home(TemplateView):
    template_name = 'index.html'

    
    def get_context_data(self, **kwargs):
        figure = folium.Figure()
        map = geemap.Map(center=[40,-100], zoom=4)

        image = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR').filterDate('2021-10-01', '2021-10-31').min()

        #NDVI
        nir = image.select('B5')
        red = image.select('B4')
        ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
        ndviParams = {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'green']}

        #EVI
        evi = image.expression(
            '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
            'NIR': image.select('B5'),
            'RED': image.select('B4'),
            'BLUE': image.select('B2')
        })
        eviParams = {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'green']}
        
        #add on map
        map.addLayer(ndvi, ndviParams, 'NDVI image')
        map.addLayer(evi, eviParams, 'EVI image')
        map.addLayerControl()
        map.add_to(figure)
        figure.render()
        #return map
        return {"map": figure}