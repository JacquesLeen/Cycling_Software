import requests
from bs4 import BeautifulSoup
import gpxpy
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from meteostat import Stations, Daily, Hourly
import sys
import json
from datetime import datetime

sys.path.insert(0,"/Users/giacomolini/Desktop/Cycling_Software/repo_results")
import Extract_from_json
sys.path.insert(0,"/Users/giacomolini/Desktop/Cycling_Software/repo_routes")
import Analyzer


track_num =['324148', '324149', '324150', '324151', '324215', '324222', '324226']

track_num = [int(x) for x in track_num]


routes_data= pd.DataFrame(columns = [
    'Race Name', 'RL', 'Elev', 'Elev/Km', 'TT', 'Ov1500m', 'Ov1800m', 'Ov2000m', 'UphFinish', 'HillFinish',
    'Quant0.25','Quant0.5', 'Quant0.6', 'Quant0.75', 'Quant0.8', 'Quant0.9', 'Quant0.95','PercFlat',
    'PercFF Up', 'PercFF Down', 'PercUp', 'PercDown', 'PercOv500m', 'PercOv1000m', 'PercOv1500m',
    'PercOv2000m', 'Avg Temp', 'Avg Wind', 'mm Prec', 'Weather Code'
])

for obj in track_num:
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

json_name = 'repo_results/14.json' #set new json name if necessary or list over files

EFJS = Extract_from_json.Extract_from_json(json_name)

rider_data = pd.DataFrame(columns = [
    'Rider Name', 'Nation Code', 'Team ID',
    'Team Name', 'Final Result', 'Final Time Gap', 'Final Result Time',
    'Stages Results', 'Stages Gaps', 'Finished Race'
])
for rider in EFJS.Riders():
    list_temp = []
    list_temp.append(EFJS.Get_Rider_Name(rider)), 
    list_temp.append(EFJS.Get_Rider_Nation_Code(rider)), 
    list_temp.append(EFJS.Get_Rider_Team_Id(rider)),
    list_temp.append(EFJS.Get_Rider_Team_Name(rider)),
    list_temp.append(EFJS.Get_Final_Result_Position(rider)),
    list_temp.append(EFJS.Get_Final_Time_Gap(rider)),
    list_temp.append(EFJS.Get_Final_Result_Time(rider)),
    list_temp.append(EFJS.Get_Stages_Results(rider)),
    list_temp.append(EFJS.Get_Stages_Gaps(rider)),
    list_temp.append(EFJS.Get_Finished_Race(rider)),
    rider_data.loc[len(rider_data)] = list_temp 
    
 
print(rider_data)

