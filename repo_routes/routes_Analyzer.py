import requests
from bs4 import BeautifulSoup
import gpxpy
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import Analyzer
from meteostat import Stations, Daily, Hourly


track_num =['383863', '375303', '383865', '322123', '383868', '322158', '386340' ]

"""'383870', '383657', '383655', '386318', '383881', '382288', '375307', 
'369657', '383882', '382289', '382292', '382290', '383656', '385698', 
'385814', '322127', '369658', '383883', '383381', '383658', '385699', 
'384603', '306423', '383885', '306426', '328728', '306413', '384661', 
'384671', '328729', '369674', '328730', '386026', '369715', '328731', 
'386029', '306417', '328732', '387641', '386030', '384875', '369676', 
'386263', '328733', '385209', '386031', '388375', '388336', '306419', 
'306421', '322287', '328453', '306264', '328454', '306260', '328455', 
'306259', '390685', '385520', '306258', '385770', '390902', '390903', 
'306257', '318469', '327298', '318703', '306185', '318473', '306186', 
'318475', '391237', '391235', '306255', '318477', '391238', '391236', 
'392635', '392177', '318481', '393027', '306253', '392363', '393424', 
'393803', '318501', '394253', '318508', '394553', '318514', '394871', 
'318523', '395245', '318533', '393474', '394622', '393473', '395369', 
'318560', '395733' """

track_num = [int(x) for x in track_num]


routes_data= pd.DataFrame(columns = [
    'Race Name', 'RL', 'Elev', 'Elev/Km', 'TT', 'Ov1500m', 'Ov1800m', 'Ov2000m', 'UphFinish', 'HillFinish',
    'Quant0.25','Quant0.5', 'Quant0.6', 'Quant0.75', 'Quant0.8', 'Quant0.9', 'Quant0.95','PercFlat',
    'PercFF Up', 'PercFF Down', 'PercUp', 'PercDown', 'PercOv500m', 'PercOv1000m', 'PercOv1500m',
    'PercOv2000m', 'Max Temperature', 'Min Temperature', 'Temperature', 'Max Feelslike', 'Min Feelslike', 'Feelslike',
    'Dew Point', 'Humidity','Precipitation','Precip Cover','Precip Type','Snow', 'Wind Gust', 'Wind Speed', 'Wind Direction', 
    'Sea Level Pressure','Conditions', 'Description'
])

"""
dir = 'gpx/'
file_list = []
for entry in os.scandir(dir):
    if (entry.path.endswith('gpx') and entry.is_file()):
        name = (entry.name)
        file_list.append(int(os.path.splitext(name)[0]) )
"""

for obj in track_num[0:5]:
    temp = Analyzer.Analyzer(obj)
    list_temp = []
    list_temp.append(list(temp.data[0].keys())[0])              ## add Name
    list_temp.append(temp.get_distance())                       ## add distance
    list_temp.append(round (list(temp.data[0].values())[0][0], 2))         ## add elevation
    list_temp.append(temp.elev_per_km())                        ## elevation per km
    list_temp.append(temp.is_tt())                              ## is Time Trial
    list_temp.append(temp.is_over_1500())                       ## is over 1500m
    list_temp.append(temp.is_over_1800())                       ## is over 1800m
    list_temp.append(temp.is_over_2000())                       ## is over 2000m
    list_temp.append(temp.is_uphill_finish())                   ## is uphill finish
    list_temp.append(temp.is_hilly_finish())                    ## is hilly finish
    list_temp.append(temp.quantile(0.25))                       ## sample quantiles
    list_temp.append(temp.quantile(0.50))
    list_temp.append(temp.quantile(0.60))
    list_temp.append(temp.quantile(0.75))
    list_temp.append(temp.quantile(0.80))
    list_temp.append(temp.quantile(0.90))
    list_temp.append(temp.quantile(0.95))
    list_temp.append(temp.flat_perc())                          ## % flat
    list_temp.append(temp.false_flat_up_perc())                 ## % ffuphill
    list_temp.append(temp.false_flat_dn_perc())                 ## % ffdownhill
    list_temp.append(temp.uphill_perc())                        ## % uphill
    list_temp.append(temp.downhill_perc())                      ## % downhill
    list_temp.append(temp.perc_over(500))                       ## % over 500m
    list_temp.append(temp.perc_over())                          ## % over 1000m
    list_temp.append(temp.perc_over(1500))                      ## % over 1500m
    list_temp.append(temp.perc_over(2000))                      ## % over 2000m
    weather_data =temp.get_weather_data()                       ## weather data
    list_temp.append(weather_data['Max Temperature'][0])
    list_temp.append(weather_data['Min Temperature'][0])
    list_temp.append(weather_data['Temperature'][0])
    list_temp.append(weather_data['Max Feelslike'][0])
    list_temp.append(weather_data['Min Feelslike'][0])
    list_temp.append(weather_data['Feelslike'][0])
    list_temp.append(weather_data['Dew Point'][0])
    list_temp.append(weather_data['Humidity'][0])
    list_temp.append(weather_data['Precipitation'][0])
    list_temp.append(weather_data['Precip Cover'][0])
    list_temp.append(weather_data['Precip Type'][0])
    list_temp.append(weather_data['Snow'][0])
    list_temp.append(weather_data['Wind Gust'][0])
    list_temp.append(weather_data['Wind Speed'][0])
    list_temp.append(weather_data['Wind Direction'][0])
    list_temp.append(weather_data['Sea Level Pressure'][0])
    list_temp.append(weather_data['Conditions'][0])
    list_temp.append(weather_data['Description'][0])
    routes_data.loc[len(routes_data)] = list_temp               ## add list to df

routes_data.to_csv('test_090922.csv')
#print(routes_data)


