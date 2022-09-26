import requests
from bs4 import BeautifulSoup
import gpxpy
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import Analyzer
from meteostat import Stations, Daily, Hourly

races = pd.read_csv(r'C:\Users\yd26114\Desktop\Cycling_Software\repo_calendar_lfr\LFR_Calendar_Info.csv') #modify code and path for actual table in the db

#filter for month and year
races = races[races['Date'].str.match('2022')]
races = races[races['Track Code'] != 'xxxxxxx']
track_num = list(races['Track Code'])


#track_num = [int(x) for x in track_num]
#track_num= [487257]


routes_data= pd.DataFrame(columns = [
    'Track Num','Race Name', 'RL', 'Elev', 'Elev/Km', 'TT', 'Ov1500m', 'Ov1800m', 'Ov2000m', 'UphFinish', 'HillFinish',
    'Quant0.25','Quant0.5', 'Quant0.6', 'Quant0.75', 'Quant0.8', 'Quant0.9', 'Quant0.95','PercFlat',
    'PercFF Up', 'PercFF Down', 'PercUp', 'PercDown', 'PercOv500m', 'PercOv1000m', 'PercOv1500m',
    'PercOv2000m', 'Date','Max Temperature', 'Min Temperature', 'Temperature', 'Max Feelslike', 'Min Feelslike', 'Feelslike',
    'Dew Point', 'Humidity','Precipitation','Precip Cover','Precip Type','Snow', 'Wind Gust', 'Wind Speed', 'Wind Direction', 
    'Sea Level Pressure','Conditions', 'Description'
])



for obj in track_num:
    print('track num', obj)
    temp = Analyzer.Analyzer(obj)
    list_temp = []
    list_temp.append(obj)
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
    date = races[races['Track Code'] == str(obj)]['Date'].item()
    print(date)
    list_temp.append(date)
    weather_data =temp.get_weather_data(date=date)              ## weather data
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

routes_data.to_csv('test_140922.csv')
print(routes_data)