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
import pickle 

sys.path.insert(0, r"/Users/giacomolini/Desktop/Cycling_Software/repo_results") #C:\Users\igord\Documents\PyCycling\Cycling_Software\repo_results
import Extract_from_json
sys.path.insert(0, r"/Users/giacomolini/Desktop/Cycling_Software/repo_routes") #C:\Users\igord\Documents\PyCycling\Cycling_Software\repo_routes
import Analyzer

#Encodes DataFrames to Json without serialising issues
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json(orient='records')
        return json.JSONEncoder.default(self, obj)

"""
    it takes some 5 minutes to run the script for downloading the tracks and since we are testing the
    merge it makes sense to download it once and save the data on a csv file which we will reupload
    directly from the local folder... 
"""

## UNCOMMENT FROM DOWN HERE IF U WISH TO LAUNCH THE WHOLE PROCESS

"""
track_num =['324148', '324149', '324150', '324151', '324215', '324222', '324226']

track_num = [int(x) for x in track_num]


routes_data= pd.DataFrame(columns = [
    'Race Name', 'RL', 'Elev', 'Elev/Km', 'TT', 'Ov1500m', 'Ov1800m', 'Ov2000m', 'UphFinish', 'HillFinish',
    'Quant0.25','Quant0.5', 'Quant0.6', 'Quant0.75', 'Quant0.8', 'Quant0.9', 'Quant0.95','PercFlat',
    'PercFF Up', 'PercFF Down', 'PercUp', 'PercDown', 'PercOv500m', 'PercOv1000m', 'PercOv1500m',
    'PercOv2000m', #'Avg Temp', 'Avg Wind', 'mm Prec', 'Weather Code'
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
    #weather_data = temp.get_weather_data()                       ## weather data
    #list_temp.append(weather_data.iloc[0,0])                    ## avg temperature
    #list_temp.append(weather_data.iloc[0,6])                    ## avg wind
    #list_temp.append(weather_data.iloc[0,3])                    ## total precipitation
    #list_temp.append(weather_data.iloc[0,10])                   ## weather code
    routes_data.loc[len(routes_data)] = list_temp               ## add list to df

routes_data.to_csv("Routes_Data.csv")
"""
json_name = 'repo_results/14.json' #set new json name if necessary or list over files

EFJS = Extract_from_json.Extract_from_json(json_name)

race_dict = {}
for i in range(EFJS.Get_Number_Of_Stages()):
    Stage_DF = pd.DataFrame(columns = [
        'Race Name','Rider Name', 'Nation Code', 'Team ID',
        'Team Name',  'Stage Result', 'Stage Time','Stage Gap', 
        'Percentage of Winning Time'
    ])
    for rider in EFJS.Riders():
        list_temp = []
        list_temp.append(EFJS.Get_Race_Name() + ' Stage '+ str(i+1))
        list_temp.append(EFJS.Get_Rider_Name(rider)), 
        list_temp.append(EFJS.Get_Rider_Nation_Code(rider)), 
        list_temp.append(EFJS.Get_Rider_Team_Id(rider)),
        list_temp.append(EFJS.Get_Rider_Team_Name(rider)),
        list_temp.append(EFJS.Get_Single_Stage_Result(rider, i+1)),
        list_temp.append(EFJS.Get_Stage_Time(rider, i+1)),
        list_temp.append(EFJS.Get_Single_Stage_Gap(rider, i+1 )),
        list_temp.append(EFJS.Get_Percentage_Of_Winning_Time(rider, i+1)),
        
        Stage_DF.loc[len(Stage_DF)] = list_temp 
    race_dict['stage'+str(i+1)] = Stage_DF


Overall_DF = pd.DataFrame(columns= [
    'Race Name','Rider Name', 'Nation Code', 'Team ID',
    'Team Name', 'Final Result', 'Final Time Gap','Final Result Time',
    'Finished Race', 'Total Percentage of Time'
])
for rider in EFJS.Riders():
    list_temp = []
    list_temp.append(EFJS.Get_Race_Name() + ' Overall')
    list_temp.append(EFJS.Get_Rider_Name(rider)), 
    list_temp.append(EFJS.Get_Rider_Nation_Code(rider)), 
    list_temp.append(EFJS.Get_Rider_Team_Id(rider)),
    list_temp.append(EFJS.Get_Rider_Team_Name(rider)),
    list_temp.append(EFJS.Get_Final_Result_Position(rider)),
    list_temp.append(EFJS.Get_Final_Time_Gap(rider)),
    list_temp.append(EFJS.Get_Final_Result_Time(rider)),
    list_temp.append(EFJS.Get_Finished_Race(rider)),
    list_temp.append(EFJS.Get_Percentage_Of_Total_Time(rider))
    Overall_DF.loc[len(Overall_DF)] = list_temp 
race_dict['Overall'] = Overall_DF

with open('Riders_Data.pkl', 'wb') as f:
    pickle.dump(race_dict, f)

## NO NEED TO IMPORT THESE FILES IF YOU UNCOMMENTED ABOVE
routes_data = pd.read_csv("Routes_Data.csv")
#race_dict = pd.read_pickle("Riders_Data.pkl")

##creates id for the races
race_id = []

for i in routes_data['Race Name']:
    race_id.append(id(i))

routes_data['ID'] = race_id

counter = 0
routes_data = routes_data[routes_data.columns.drop('Unnamed: 0')]
routes_data = routes_data[routes_data.columns.drop('Race Name')]

race_final = {}

for stage in race_dict:
    if 'stage' in stage:
        counter = counter +1
        temp = pd.DataFrame(columns = [
                            'RL', 'Elev', 'Elev/Km', 'TT', 'Ov1500m', 'Ov1800m', 'Ov2000m', 'UphFinish', 'HillFinish',
                            'Quant0.25','Quant0.5', 'Quant0.6', 'Quant0.75', 'Quant0.8', 'Quant0.9', 'Quant0.95','PercFlat',
                            'PercFF Up', 'PercFF Down', 'PercUp', 'PercDown', 'PercOv500m', 'PercOv1000m', 'PercOv1500m',
                            'PercOv2000m', 'ID', #'Avg Temp', 'Avg Wind', 'mm Prec', 'Weather Code'
                            ])
        elem_to_add = list(routes_data.loc[counter-1])
        for i in range(len(race_dict[stage])):
            temp.loc[i]=elem_to_add
        final = pd.concat([race_dict[stage], temp], axis=1, join= "inner")
        race_final['Stage - '+str(stage)]= final

race_final['Overall']= race_dict['Overall']

data_dict = {
    key: race_final[key].to_dict(orient='records') 
    for key in race_final.keys()
}

# write to disk
with open('race_final.json', 'w') as fp:
    json.dump(
        data_dict, 
        fp, 
        indent=4, 
        sort_keys=True
    )
