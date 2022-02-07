# Green Cover

_This project serves as backend for [Green Cover (green-cover-frontend)](https://github.com/VirajPatidar/green-cover-frontend)._ <br/>
_green-cover is a project that helps in analysing geo-mapped aerial data to estimate green cover and related factors._ <br/>

<br/>

**Link to the website:** [https://green-cover.netlify.app/](https://green-cover.netlify.app/) <br/>

**Link to frontend repo:** [https://github.com/VirajPatidar/green-cover-frontend](https://github.com/VirajPatidar/green-cover-frontend)


### Tech Stack ###
**Vision Analytics, Machine Learning, Datasets and Satellite Imagery:**
* [Google Earth Engine Datasets](https://developers.google.com/earth-engine/datasets)
* [Google Earth Engine Python API](https://earthengine.google.com/)
* [Geemap](https://geemap.org/)


**Backend and API:**
* [Django](https://www.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [Voila](https://github.com/voila-dashboards/voila)


### Features ###
* Analysis of geo mapped photographs and satellite imagery to estimate green cover over time across the globe.
* Rendering dynamic maps to analyse green cover and generate timelapses representing change in green cover.
* To understand how increasing rate of deforestation is directly related to bad air quality and provide concrete statistics for the same. 
* Time series chart/graph representing change in green cover over the years for the state of Maharashtra.
* Predicting type of landcover in the state of Maharashtra by performing supervised classification using existing datasets. 
* Analysis of air quality on basis of various parameters for the state of Maharashtra.
* A system to manage and sign-up volunteers to arrange green drives and awareness programs.


### Features along with datasets used: ###

| TASK / FEATURE | DATASET |
| :---         | :---         
| Estimating Green Cover using Vegetation Indexes (Global)   | <ul><li> [USGS Landsat 8 Level 2, Collection 2, Tier 1](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2) </li></ul>   |
| Timelapse for Normalized Difference Vegetation Index (NDVI) (Global)     | <ul><li> [USGS Landsat 8 Level 2, Collection 2, Tier 1](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2) </li><li> [USGS Landsat 5 Level 2, Collection 2, Tier 1](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C02_T1_L2) </li></ul> |
| Time series graphical analysis representing Vegetation Indexes (NDVI & EVI) of Maharashtra     | <ul><li> [MOD13Q1.006 MODIS Terra Vegetation Indices 16-Day Global 250m](https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13Q1) </li></ul>     |
| Landcover Analysis of Maharashtra     | <ul><li> [USGS Landsat 8 Level 2, Collection 2, Tier 1](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2) </li><li> [MCD12Q1.006 MODIS Land Cover Type Yearly Global 500m](https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD12Q1) </li></ul>  |
| Analysing Air Quality of Maharashtra     | <ul><li> [Sentinel-5P NRTI AER AI: Near Real-Time UV Aerosol Index](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_NRTI_L3_AER_AI) </li><li> [Sentinel-5P NRTI CO: Near Real-Time Carbon Monoxide](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_NRTI_L3_CO) </li><li> [Sentinel-5P NRTI NO2: Near Real-Time Nitrogen Dioxide](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_NRTI_L3_NO2) </li><li> [Sentinel-5P NRTI HCHO: Near Real-Time Formaldehyde](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_NRTI_L3_HCHO) </li></ul>  |

<br/>

**Custom Map API:**
| Method | API Endpoint | Description |
| :---         | :---         | :--- 
| `GET` | `/vegetation` | To get vegetation map and related data |
| `GET` | `/ndvitimelapse` | To get NDVI timelapse map and related data |
| `GET` | `/landcover` | To get landcover map and related data |
| `GET` | `/landcoverclassification` | To get land cover classification data (area & change) from 2001 to 2020 |
| `GET` | `/airqualityindex` | To get airquality map and related data |
| `POST` | `/vegetation` | To get NDVI and EVI graphs based on selected time range |
| `POST` | `/create-volunteer` | To create a volunteer |
| `POST` | `/get-volunteers` | To get all volunteers (admin only) |

<br/>
<br/>

