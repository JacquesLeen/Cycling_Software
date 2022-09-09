import requests
from bs4 import BeautifulSoup
import gpxpy
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import Analyzer
from meteostat import Stations, Daily, Hourly
import csv
import codecs
import urllib.request
import urllib.error
import sys

track_num =['288697']
#track_num = [int(x) for x in track_num]

for obj in track_num:
    temp = Analyzer.Analyzer(obj)
    #temp.get_gpx_file()
    temp.get_data_from_gpx()
    print(temp.get_weather_data())