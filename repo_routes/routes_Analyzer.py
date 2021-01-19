import requests
from bs4 import BeautifulSoup
import gpxpy
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import Analyzer

routes_data= pd.DataFrame(columns = [
    'Race Name', 'Race Length', 'Elevation', 'Elevation/Km', 'TT', 'Over 1500m', 'Over 1800m', 'Over 2000m', 'Uphill Finish', 'Hilly finish',
    'Quantile 0.25','Quantile 0.5', 'Quantile 0.6', 'Quantile 0.75', 'Quantile 0.8', 'Quantile 0.9', 'Quantile 0.95',' Perc Flat',
    'Perc False Flat Up', 'Perc False Flat Down', 'Perc Uphill', 'Perc Downhill', 'Perc over 500m', 'Perc over 1000m', 'Perc over 1500m',
    'Perc over 2000m'
])

dir = 'gpx/'
file_list = []
for entry in os.scandir(dir):
    if (entry.path.endswith('gpx') and entry.is_file()):
        name = (entry.name)
        file_list.append(int(os.path.splitext(name)[0]) )


for obj in file_list[40:60]:
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
    routes_data.loc[len(routes_data)] = list_temp               ## add list to df


print(routes_data)
