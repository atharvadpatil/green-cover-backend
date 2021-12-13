import os
from django.shortcuts import render
from django. conf import settings

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

#graph imports
import numpy as np
import pandas as pd
import proplot as plot 
import matplotlib.pyplot as plt 
from ipygee import chart
from pandas.plotting import register_matplotlib_converters

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


def scale_factor(image):
  return image.multiply(0.0001).copyProperties(image, ['system:time_start'])


class vegetationView(generics.GenericAPIView):
    def get(self, request):
        dataset_list=["USGS Landsat 8 Level 2, Collection 2, Tier 1"]

        data_dict = {
            'map_url': 'http://localhost:8866/voila/render/Vegetation.ipynb',
            'dataset': dataset_list
        }

        return Response({'response_data':data_dict}, status=status.HTTP_200_OK)

    
    def post(self, request):
        start_date = request.data.get('start_date', '')
        end_date = request.data.get('end_date', '')
        st_date = start_date.replace("-", "")
        ed_date = end_date.replace("-", "")
        if int(st_date)> int(ed_date):
            return Response({"message":"Start date should not be greater than End date"}, status=status.HTTP_400_BAD_REQUEST)
        

        path_ndvi = os.path.join(settings.MEDIA_ROOT, "ndvi_graph.png")
        path_evi = os.path.join(settings.MEDIA_ROOT, "evi_graph.png")
        path_indexes = os.path.join(settings.MEDIA_ROOT, "indexes_graph.png")

        if os.path.exists(path_ndvi):
                os.remove(path_ndvi)

        if os.path.exists(path_evi):
                os.remove(path_evi)

        if os.path.exists(path_indexes):
                os.remove(path_indexes)

        admin2 = ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level2")
        Maharashtra = admin2.filter(ee.Filter.eq('ADM1_NAME', 'Maharashtra'))

        modis = ee.ImageCollection('MODIS/006/MOD13Q1')
        start_date = request.data.get('start_date', '')
        modis = modis.filterDate(ee.DateRange(start_date, end_date))

        evi = modis.select('EVI')
        ndvi = modis.select('NDVI')

        scaled_evi = evi.map(scale_factor)
        scaled_ndvi = ndvi.map(scale_factor)

        m_ndvi = chart.Image.series(**{'imageCollection': scaled_ndvi,
                                        'region': Maharashtra,
                                        'reducer': ee.Reducer.mean(),
                                        'scale': 1000,
                                        'xProperty': 'system:time_start'})
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(m_ndvi.dataframe.index, m_ndvi.dataframe['NDVI'],
                color='forest green', marker='o')
        ax.set_ylabel('NDVI')
        plt.savefig(path_ndvi, dpi=300)

        m_evi = chart.Image.series(**{'imageCollection': scaled_evi,
                                   'region': Maharashtra,
                                   'reducer': ee.Reducer.mean(),
                                   'scale': 1000,
                                   'xProperty': 'system:time_start'})

        fig, ax = plot.subplots(figsize=(10, 4))
        ax.plot(m_evi.dataframe.index, m_evi.dataframe['EVI'],
                color='brown', marker='+')
        ax.set_ylabel('EVI')
        plt.savefig(path_evi, dpi=300)

        # monthly averaging
        m_evi_monthly = m_evi.dataframe.groupby(pd.Grouper(freq="M")).mean()
        m_ndvi_monthly = m_ndvi.dataframe.groupby(pd.Grouper(freq="M")).mean()

        # time index
        time = m_evi_monthly.index
        # plot
        fig, ax1 = plt.subplots(figsize=(10, 4))
        ax2 = ax1.twinx()
        # EVI
        ax1.plot(time, m_evi_monthly, label='EVI',
                color='brown', marker='+')
        # NDVI
        ax2.plot(time, m_ndvi_monthly, label='NDVI',
                color='forest green', marker='o')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('EVI')
        ax2.set_ylabel('NDVI')
        ax1.set_yticks(np.arange(0.0, 1.1, 0.1))
        ax2.set_yticks(np.arange(0.0, 1.1, 0.1))
        plt.legend()
        plt.tight_layout()
        plt.savefig(path_indexes, dpi=300)

        return Response({
            'ndvi_graph':"http://127.0.0.1:8000/media/ndvi_graph.png",
            'evi_graph':"http://127.0.0.1:8000/media/evi_graph.png",
            'indexes_graph':"http://127.0.0.1:8000/media/indexes_graph.png"    
        }, status=status.HTTP_200_OK)