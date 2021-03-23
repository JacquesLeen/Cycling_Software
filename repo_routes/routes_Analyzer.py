import requests
from bs4 import BeautifulSoup
import gpxpy
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import Analyzer
from meteostat import Stations, Daily, Hourly




routes_data= pd.DataFrame(columns = [
    'Race Name', 'RL', 'Elev', 'Elev/Km', 'TT', 'Ov1500m', 'Ov1800m', 'Ov2000m', 'UphFinish', 'HillFinish',
    'Quant0.25','Quant0.5', 'Quant0.6', 'Quant0.75', 'Quant0.8', 'Quant0.9', 'Quant0.95','PercFlat',
    'PercFF Up', 'PercFF Down', 'PercUp', 'PercDown', 'PercOv500m', 'PercOv1000m', 'PercOv1500m',
    'PercOv2000m', 'Avg Temp', 'Avg Wind', 'mm Prec', 'Weather Code'
])

dir = 'gpx/'
file_list = []
for entry in os.scandir(dir):
    if (entry.path.endswith('gpx') and entry.is_file()):
        name = (entry.name)
        file_list.append(int(os.path.splitext(name)[0]) )


for obj in file_list[0:10]:
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
    list_temp.append(weather_data.iloc[0,0])                    ## avg temperature
    list_temp.append(weather_data.iloc[0,6])                    ## avg wind
    list_temp.append(weather_data.iloc[0,3])                    ## total precipitation
    list_temp.append(weather_data.iloc[0,10])                   ## weather code
    routes_data.loc[len(routes_data)] = list_temp               ## add list to df


print(routes_data)


