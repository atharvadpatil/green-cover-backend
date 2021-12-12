from django.shortcuts import render

#rest import
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response

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


class airQualityIndexView(generics.GenericAPIView):
    def get(self, request):
        dataset_list=["Sentinel-5P NRTI AER AI: Near Real-Time UV Aerosol Index", "Sentinel-5P NRTI CO: Near Real-Time Carbon Monoxide", "Sentinel-5P NRTI NO2: Near Real-Time Nitrogen Dioxide", "Sentinel-5P NRTI HCHO: Near Real-Time Formaldehyde"]

        data_dict = {
            'map_url': 'http://localhost:8866/voila/render/AirQualityIndex.ipynb',
            'dataset': dataset_list
        }

        return Response({'response_data':data_dict}, status=status.HTTP_200_OK)



class landCoverView(generics.GenericAPIView):
    def get(self, request):
        dataset_list=["USGS Landsat 8 Level 2, Collection 2, Tier 1", "MCD12Q1.006 MODIS Land Cover Type Yearly Global 500m"]

        data_dict = {
            'map_url': 'http://localhost:8866/voila/render/LandCover.ipynb',
            'dataset': dataset_list
        }

        return Response({'response_data':data_dict}, status=status.HTTP_200_OK)


class ndviTimelapseView(generics.GenericAPIView):
    def get(self, request):
        dataset_list=["MOD13Q1.006 MODIS Terra Vegetation Indices 16-Day Global 250m"] #check dataset for add_landsat_ts_gif 

        data_dict = {
            'map_url': 'http://localhost:8866/voila/render/NdviTimelapse.ipynb',
            'dataset': dataset_list
        }

        return Response({'response_data':data_dict}, status=status.HTTP_200_OK)

class vegetationView(generics.GenericAPIView):
    def get(self, request):
        dataset_list=["USGS Landsat 8 Level 2, Collection 2, Tier 1"]

        data_dict = {
            'map_url': 'http://localhost:8866/voila/render/Vegetation.ipynb',
            'dataset': dataset_list
        }

        return Response({'response_data':data_dict}, status=status.HTTP_200_OK)