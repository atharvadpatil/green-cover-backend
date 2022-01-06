import os
from django.shortcuts import render
from django. conf import settings
from django.contrib.auth import authenticate, login, logout
import datetime

#rest import
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response

#serializers
from .serializers import (
    VolunteerSerializer,
    EventSerializer
)

#models
from .models import Volunteer, Event

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


#import from other file
from .utils import Util

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
            'name': 'Air Quality Analysis of Maharashtra',
            'description': 'Map representing air quality of Maharashtra',
            'map_url': 'http://localhost:8866/voila/render/AirQualityIndex.ipynb',
            'dataset': dataset_list,
            'dataset_url': ['https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_NRTI_L3_AER_AI', 'https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_NRTI_L3_CO', 'https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_NRTI_L3_NO2', 'https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_NRTI_L3_HCHO'],

            'instructions': 'The rendered map is pannable and zoomable, use it accordingly\\nClick on the globe icon (located top-left) to search and mark a specific location\\nRefer the legend to interpret the data presented on the map\\nClick on the toolbar on the top-right corner and select layers to switch between layers (Absorbing Aerosol Index (AAI), Carbon monoxide (CO), Nitrogen oxides (NO2 and NO), AtmosphericFormaldehyde (HCHO) and google maps).\\nUse the slider alongside to adjust the opacity'

        }

        return Response({'response_data':data_dict}, status=status.HTTP_200_OK)



class landCoverView(generics.GenericAPIView):
    def get(self, request):
        dataset_list=["USGS Landsat 8 Level 2, Collection 2, Tier 1", "MCD12Q1.006 MODIS Land Cover Type Yearly Global 500m"]

        data_dict = {
            'name': 'Landcover Analysis of Maharashtra',
            'description': 'Map representing predicted landcover of Maharashtra using supervised classification technique',
            'map_url': 'http://localhost:8866/voila/render/LandCover.ipynb',
            'dataset': dataset_list,
            'dataset_url': ['https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2', 'https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD12Q1'],

            'instructions': 'The rendered map is pannable and zoomable, use it accordingly\\nClick on the globe icon (located top-left) to search and mark a specific location\\nRefer the legend to interpret the data presented on the map\\nClick on the toolbar on the top-right corner and select layers to switch between layers (landsat8, training points, landcover(result), original MODIS for comparision and google maps).\\nUse the slider alongside to adjust the opacity'
        }

        return Response({'response_data':data_dict}, status=status.HTTP_200_OK)


class ndviTimelapseView(generics.GenericAPIView):
    def get(self, request):
        dataset_list=["USGS Landsat 8 Level 2, Collection 2, Tier 1", "USGS Landsat 5 Level 2, Collection 2, Tier 1"] 

        data_dict = {
            'name': 'Timelapse for Normalized Difference Vegetation Index (NDVI) (Global)',
            'description': 'Map to generate timelapse for Normalized Difference Vegetation Index (NDVI) (Global) of selected region',
            'map_url': 'http://localhost:8866/voila/render/NdviTimelapse.ipynb',
            'dataset': dataset_list,
            'dataset_url': ['https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2', 'https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C02_T1_L2'],

            'instructions': 'The rendered map is pannable and zoomable, use it accordingly\\nClick on the globe icon (located top-left) to search and mark a specific location\\nA darker shade of green represents more vegetation and lighter or blue shade represents less or no vegetation respectively\\nUse the rectangular selection tool present on the left side of the map to define the boundary for the timelapse\\nSelect the start year, start month, end year and end month from the sliders provided\\nClick on the create timelapse button and wait patiently ⏰ (2 mins) to see the timplase GIF render on the map itself\\nClick on the toolbar and click on layers. Select the secondary layer icon below and uncheck timelapse ND to see the timelapse without contrast.',
        }

        return Response({'response_data':data_dict}, status=status.HTTP_200_OK)


def scale_factor(image):
  return image.multiply(0.0001).copyProperties(image, ['system:time_start'])


class vegetationView(generics.GenericAPIView):
    def get(self, request):
        dataset_list=["USGS Landsat 8 Level 2, Collection 2, Tier 1"]

        data_dict = {
            'name': 'Estimating Green Cover using Vegetation Indexes (Global)',
            'description': 'Map representing green cover for desired MM/YYYY based on NDVI and EVI indexes',
            'map_url': 'http://localhost:8866/voila/render/Vegetation.ipynb',
            'dataset': dataset_list,
            'dataset_url': 'https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2',

            'instructions': 'The rendered map is pannable and zoomable, use it accordingly\\nClick on the globe icon (located top-left) to search and mark a specific location\\nA darker shade of green represents more vegetation and lighter or blue shade represents less or no vegetation respectively\\nClick on the toolbar on the top-right corner and select layers to switch between layers (NDVI, NVI and google maps).\\nUse the slider alongside to adjust the opacity\\nSelect the year(Y) and month(M) to get the respective map for that month (01-MM-YYYY to 30-MM-YYYY)'
            
        }

        return Response({'response_data':data_dict}, status=status.HTTP_200_OK)

    
    def post(self, request):
        start_date = request.data.get('start_date', '')
        end_date = request.data.get('end_date', '')
        st_date = start_date.replace("-", "")
        ed_date = end_date.replace("-", "")

        if int(st_date) < 20020218 or int(ed_date) < 20020218:
            return Response({"message":"Date must be greater than 2002-02-18"}, status=status.HTTP_400_BAD_REQUEST)

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


class VolunteerView(generics.GenericAPIView):
    serializer_class = VolunteerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        volunteer_data = serializer.data

        volunteer = Volunteer.objects.get(email=volunteer_data['email'])
        to_email=[volunteer.email]
        email_body = "Hello "+volunteer.name+",\n\nWelcome to Green Cover Analytics Tool, a initiative by team Binary\n"+"Thank you for becoming a volunteer.\nWe will contact you soon regarding our green drive to reduce green cover depletion and spread awareness in "+ volunteer.city+", Maharashtra-"+ str(volunteer.pincode) +".\n\nThanks and Regards,\nTeam Binary"
        data = {'email_body': email_body, 'to_email': to_email,
                'email_subject': 'Welcome'}

        Util.send_email(data)
        return Response(volunteer_data, status=status.HTTP_201_CREATED)


class AdminView(generics.GenericAPIView):
    serializer_class = VolunteerSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'response':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        volunteers = Volunteer.objects.all().order_by('city')
        volunteers_serializer = VolunteerSerializer(instance=volunteers, many=True)

        return Response(volunteers_serializer.data,  status=status.HTTP_200_OK)


class EventView(generics.GenericAPIView):
    serializer_class = EventSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        event_data = serializer.data
        if event_data["notify"]:
            city = event_data["city"]
            email_list = list(Volunteer.objects.values_list('email', flat=True).filter(city=city))
            email_body = "Team Binary invites you to join campaign in your city.\nDeatils are give below:\nName of campaign:"+event_data["name"]+"\nAddress:"+event_data["address"]+"\nDate:"+event_data["date"]+"\nInstructions:"+event_data["details"]+"\n\nThanks and Regards,\nTeam Binary"
            data = {'email_body': email_body, 'to_email': email_list,
                'email_subject': 'Invitation To campaign'}
            Util.send_email(data)
        return Response(event_data, status=status.HTTP_201_CREATED)




class GetEventView(generics.GenericAPIView):
    serializer_class = EventSerializer

    def get(self, request):

        upcoming_events = Event.objects.filter(date__gt = datetime.datetime.now().date()).order_by('-date')[:5]

        upcoming_events_serializer = EventSerializer(instance=upcoming_events, many=True)

        return Response(upcoming_events_serializer.data,  status=status.HTTP_200_OK)


class StatiscticsView(generics.GenericAPIView):

    def get(self, request):
        
        volunteers_count = Volunteer.objects.count()
        total_events_count = Event.objects.count()
        upcoming_events_count = Event.objects.filter(date__gt = datetime.datetime.now().date()).count()
        trees_planted = 212
        
        resp = {
                    'volunteers': volunteers_count,
                    'planted': trees_planted,
                    'total_events': total_events_count,
                    'upcoming_events': upcoming_events_count,
                }

        return Response(resp, status=status.HTTP_200_OK)
