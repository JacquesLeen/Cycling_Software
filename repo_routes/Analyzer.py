from bs4 import BeautifulSoup
import requests
from haversine import haversine, Unit
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from datetime import datetime
import csv
import codecs
import urllib.request
import urllib.error
import sys


class Analyzer:
    def __init__(self, track_number = []):
        self.t_n= track_number
        self.data = self.get_data_from_gpx()

    def get_gpx_track(self):
        """Send request to la flamme rouge website to a specific gpx track
        
        Returns
        ------------
        The parsed URLs as a list
        """
        soup = []
        #print(self.t_n)
        for track in self.t_n:
            url = 'http://la-flamme-rouge.eu/maps/viewtrack/gpx/'+str(track)
            headers={'User-Agent':'Mozilla/5'}
            r = requests.get(url, allow_redirects=True,headers=headers)
            soup.append(BeautifulSoup(r.text,'html.parser'))
        return soup
    
    def get_elevation(self):
        """Extract stage name and elevation information from the text of the parsed URLs
    
        Parameters
        ------------
        track_html: list of parsed URLs
    
        Returns
        ------------
        A dictionary where the key is the stage name and the value is a list [positive_elevation_gain, max_elevation]
        """
        # get elevation from html
        track_html = self.get_gpx_track()
        elev_stage = {}
        for track in track_html:
            elev = [int(elev.text) for elev in track.find_all('ele')]
            name = track.find('name').text
            elev_change = sum([elev[i+1]-elev[i] for i in range(len(elev)-1) if elev[i+1]>elev[i]])
            max_elev = max(elev)
            elev_stage[name] = [elev_change, max_elev]
        return elev_stage

    def get_gpx_file(self):
        """Send request to la flamme rouge website to a specific gpx track
        saves the gpx file into "/gpx/__track_number__.gpx
        Parameters
        ------------
        track_number: list of track numbers to parse (int)
        
        Returns
        ------------
        void
        
        print(type(self.t_n))
        print(self.t_n)
        for track in self.t_n:
        """
        url = 'http://la-flamme-rouge.eu/maps/viewtrack/gpx/'+str(self.t_n)
        headers={'User-Agent':'Mozilla/5'}
        r = requests.get(url, allow_redirects=True,headers=headers)
        open('gpx/'+str(self.t_n)+'.gpx', 'wb').write(r.content)

    def get_data_from_gpx(self):
        """Extract stage name elevation, max elevation and distance as well as last point from the gpx files
    
        Returns
        ------------
        A dictionary where the key is the stage name and the value is a list [positive_elevation_gain, max_elevation, distance, [latitude, longitude]]
        """
        data_race={}
        track = self.t_n
        last_point = []
        url = 'http://la-flamme-rouge.eu/maps/viewtrack/gpx/'+str(self.t_n)
        headers = {'User-Agent':'Mozilla/5'}
        r = requests.get(url, allow_redirects=True,headers=headers)
        soup = BeautifulSoup(r.text,'html.parser')

        lat = []
        lon = []
        ele = []
        for i in soup.find('trkseg').find_all('trkpt'):
            lat.append(i['lat'])
            lon.append(i['lon'])
            ele.append(i.find('ele').text)
        race_name = soup.find('name').text
        elev_change = 0     ## sets elev_change = 0
        distance = 0
        max_elev = int(ele[0])    ## append last point (for weather data)
        last_point = [float(lat[-1]), float(lon[-1])]
    
        for i in range(1,len(ele)):                                 ## loops through all elements 
                        ## evaluate total elevation change
            if(int(float(ele[i]))>int(float(ele[i-1]))):                          ## if this point is higher than previous 
                elev_change += int(float(ele[i]))-int(float(ele[i-1]))            ## add the difference to elev_change
                        ## search for highest point in the race
            if(int(float(ele[i])) > int(float(max_elev))):                        ## if this point is higher than max_elev
                max_elev=ele[i]                                     ## set max_elev to new value
                        ## haversine distance
            begin = (float(lat[i]), float(lon[i]))
            end = (float(lat[i-1]), float(lon[i-1]))
            distance += haversine( end, begin )
        ele = [int(float(x)) for x in ele]
        data_race[race_name] = [elev_change, max_elev, distance, last_point]
        return [data_race, ele]
        
        """
        #tracks = list(self.t_n)
        #for track in tracks:
        if True:
            if os.path.isfile('gpx/'+str(self.t_n)+'.gpx'):
                file_name = 'gpx/'+str(track)+'.gpx'
                gpx_file= open(file_name, 'r')
                gpx = gpxpy.parse(gpx_file)
                name = gpx.tracks[0].name
                elev = [point.elevation for point in gpx.tracks[0].segments[0].points]
                elev_change = sum([ elev[i+1] - elev[i] for i in range(len(elev)-1) if elev[i+1] > elev[i] ])
                max_elev = max(elev)
                distance = round(gpx.length_2d()/1000,2)
                last_point.append(gpx.tracks[0].segments[0].points[-1].latitude)
                last_point.append(gpx.tracks[0].segments[0].points[-1].longitude)
                data_race[name] = [elev_change, max_elev, distance, last_point]
            else:
                print('File'+str(self.t_n),'needs to be downloaded \n',
                    'Usage: self.get_gpx_file()'
                    ) 
                return 0
        return [data_race,elev]
        """


    def is_over_1500(self)->bool:
        """
        determines whether the race got over 1500m of altitude
        """
        data = self.data
        if float(list(data[0].values())[0][1]) >= 1500:
            return True
        return False
    
    def is_over_1800(self)->bool:
        """
        determines whether the race got over 2000m of altitude
        """
        data = self.data
        if float(list(data[0].values())[0][1]) >= 1800:
            return True
        return False

    def is_over_2000(self)->bool:
        """
        determines whether the race got over 2000m of altitude
        """
        data = self.data
        if float(list(data[0].values())[0][1]) >= 2000:
            return True
        return False

    def get_distance(self)->float:
        """
        Returns the total distance in km

        Output
        -------------------------
        distance (float)
        """
        data = self.data
        return list(data[0].values())[0][2]

    def get_altitude(self, distance)->float:
        """
        Returns the altitude of a waypoint, given file name and distance at which you want to get the altitude
    
        Input
        ------------------------- 
        tracknumber (int) and distance (float, km)

        Output
        -------------------------
        altitude (float, m)
        """
        data = self.data
        waypoint = int( distance * len(data[1]) / self.get_distance() ) 

        return data[1][waypoint-1]

    def is_uphill_finish(self)->bool:
        """
        Determines whether a gpx track can be classified as (uphill finish) UF or not.
        In order to be a UF the criteria that must be met is the following (can be modified)
        -in the last 5 km of the race there has to be an average gradient of at least 4%
        -that means at least 200m of elevation    

        Output
        -------------------------
        Bool
        """
        finish = self.get_distance()
        try:
            if int(self.get_altitude(finish)) - int(self.get_altitude(finish -4)) >=160:
                return True
            else:
                return False
        except:
            return False

    def is_hilly_finish(self)->bool:
        """
        Determines whether a gpx track can be classified as (hilly finish) HF or not.
        In order to be a HF the criteria that must be met is the following (can be modified)
        -in the last 0.5 km of the race there has to be an average gradient of at least 5%
        -that means at least 25m of elevation    

        Output
        -------------------------
        Bool
        """
        finish = self.get_distance()
        if self.is_uphill_finish() == True:
            return False

        if int(self.get_altitude(finish)) - int(self.get_altitude(finish -0.5)) >=25:
            return True
        else:
            return False

    def quantile(self, percent=0.5)->float:
        """
        takes as input the tracknumber and a percent (between 0 and 1) and returns the amount of kms
        necessary to reach that percent of covered elevation. Example: quantile(306106, 0.5) takes the infos
        from track number 306106 and returns the amount of km necessary to cover half of the total positive
        elevation.

        Input
        -------------------------
        percent (float)

        Output
        -------------------------
        distance (float, km)
        """
        if (percent <0 or percent >1):
            print('Error usage: percent must be between 0-1')
            return -1
        if (percent == 0):
            return 0
        data=self.data
        elev = data[1]
        elev_change = list(data[0].values())[0][0]
        distance = list(data[0].values())[0][2]
        temp = 0
        for i in range(len(elev)-1):
            if elev[i+1] > elev[i]:
                temp += int(elev[i+1]) - int(elev[i])
                if(temp >= elev_change * percent):
                    return round(distance/len(elev) * i,2) / distance

    def flat_perc(self)->float:
        """
        Determines what % of a given parcour is to be considered flat:
        flat -> less then 2% of gradient measured over a single waypoint

        Input
        --------------------------
        self

        Output
        --------------------------
        float between 0 and 1
        """
        distance = self.get_distance()
        interval = 0.05
        temp = 0
        ascent = 2*interval /0.1
        for i in np.arange(interval, distance, interval):
            if(self.get_altitude(i) - self.get_altitude(i-interval) < ascent and self.get_altitude(i) - self.get_altitude(i-interval) > -1* ascent):
                temp+=interval
        return round(temp/distance,3)

    def false_flat_up_perc(self)->float:
        """
        Determines what % of a given parcour is to be considered false flat uphill:
        false flat uphill -> between 2 and 4 %  of gradient measured over a waypoint

        Input
        --------------------------
        self

        Output
        --------------------------
        float between 0 and 1
        """
        distance = self.get_distance()
        interval = 0.05
        temp = 0
        min_ascent = 2*interval /0.1
        max_ascent = 4*interval /0.1
        for i in np.arange(interval, distance, interval):
            if(min_ascent <= self.get_altitude(i) - self.get_altitude(i-interval) < max_ascent):
                temp+=interval
        return round(temp/distance,3) 

    def false_flat_dn_perc(self)->float:
        """
        Determines what % of a given parcour is to be considered false flat downhill:
        false flat uphill -> between -2 and -4 %  of gradient measured over a waypoint

        Input
        --------------------------
        self

        Output
        --------------------------
        float between 0 and 1
        """
        distance = self.get_distance()
        interval = 0.05
        temp = 0
        min_descent = -1* 2*interval /0.1
        max_descent = -1* 4*interval /0.1
        for i in np.arange(interval, distance, interval):
            if(max_descent < self.get_altitude(i) - self.get_altitude(i-interval) <= min_descent):
                temp+=interval
        return round(temp/distance,3)

    def downhill_perc(self)->float:
        """
        Determines what % of a given parcour is to be considered downhill:
        downhill -> more then 4% of gradient measured over a single waypoint

        Input
        --------------------------
        self

        Output
        --------------------------
        float between 0 and 1
        """
        distance = self.get_distance()
        interval = 0.05
        temp = 0
        descent = -1* 4*interval /0.1
        for i in np.arange(interval, distance, interval):
            if(self.get_altitude(i) - self.get_altitude(i-interval) <= descent):
                temp+=interval
        return round(temp/distance,3)  

    def uphill_perc(self)->float:
        """
        Determines what % of a given parcour is to be considered downhill:
        uphill -> more then 4% of gradient measured over a single waypoint

        Input
        --------------------------
        self

        Output
        --------------------------
        float between 0 and 1
        """
        distance = self.get_distance()
        interval = 0.05
        temp = 0
        ascent = 4*interval /0.1
        for i in np.arange(interval, distance, interval):
            if(ascent <= self.get_altitude(i) - self.get_altitude(i-interval)):
                temp+=interval
        return round(temp/distance,3)  

    def elev_per_km(self)->float:
        """
        Returns average elevation gained per km of race
        """
        elev = list(self.data[0].values())[0][0]
        distance = self.get_distance()
        return round(elev/distance, 3)

    def is_tt(self)->bool:
        """
        Is this race a TT ?
        """
        url = 'https://www.la-flamme-rouge.eu/maps/viewtrack/'+str(self.t_n)
        headers={'User-Agent':'Mozilla/5'}
        r = requests.get(url, allow_redirects=True,headers=headers)
        return 'Time Trial' in r.text
    
    def perc_over(self, altitude=1000)->bool:
        """
        Determines what % of the race is at a higher altitude than x (default 1000) meters
        Input
        --------------------------
        self
        target altitude (default 1000m)

        Output
        --------------------------
        float between 0 and 1
        """
        data = self.data[1]
        temp = []
        for i in data:
            if i>altitude:
                temp.append(i)
        return round(len(temp)/len(data),3)

    def get_weather_data(self, date='2019-09-29'):
        """
        Determines some weather data (metereological station closest to the final point) on the
        day of the race
        Input
        --------------------------
        self
        latitude and longitude (decimal)
        date (datetime)
        Output
        --------------------------
        dataframe
        """
        latitude = list(self.data[0].values())[0][3][0]
        longitude = list(self.data[0].values())[0][3][1]

        BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'

        ApiKey='5DKM32326GJWXTEAASSUPZZGX'

        UnitGroup= 'metric'

        Location = str(latitude) +','+str(longitude) # can be specified as a set of lat and lon coordinates, address, partial address
        #JSON or CSV 
        #JSON format supports daily, hourly, current conditions, weather alerts and events in a single JSON package
        #CSV format requires an 'include' parameter below to indicate which table section is required
        ContentType="csv"

        #if not specified start and end date, then a random day in the past or future gets returned, format is YYYY-MM-DD
        StartDate = date
        EndDate=''

        #include sections
        #values include days,hours,current,alerts
        Include="days"

        ApiQuery = BaseURL+ Location
        if(len(StartDate)):
            ApiQuery+= "/"+StartDate
            if (len(EndDate)):
                ApiQuery+= "/"+EndDate

        ApiQuery+="?" #from here on we add the query parameters
        if(len(UnitGroup)):
            ApiQuery+="&unitGroup="+UnitGroup

        if(len(ContentType)):
            ApiQuery+="&contentType="+ContentType

        if(len(Include)):
            ApiQuery+="&include="+Include

        ApiQuery+="&key="+ApiKey

        #print(' - Running query URL: ', ApiQuery)
        #print()

        try: 
            CSVBytes = urllib.request.urlopen(ApiQuery)
        except urllib.error.HTTPError  as e:
            ErrorInfo= e.read().decode() 
            print('Error code: ', e.code, ErrorInfo)
            sys.exit()
        except  urllib.error.URLError as e:
            ErrorInfo= e.read().decode() 
            print('Error code: ', e.code,ErrorInfo)
            sys.exit()

        CSVText = csv.reader(codecs.iterdecode(CSVBytes, 'utf-8'))
        RowIndex = 0
        # The first row contain the headers and the additional rows each contain the weather metrics for a single day
        # To simply our code, we use the knowledge that column 0 contains the location and column 1 contains the date.  The data starts at column 4
        df = pd.DataFrame(columns=[
            'Max Temperature', 'Min Temperature', 'Temperature', 'Max Feelslike', 'Min Feelslike', 'Feelslike', 'Dew Point', 'Humidity','Precipitation', 'Precip Prob', 'Precip Cover', 'Precip Type',
            'Snow', 'Snow depth', 'Wind Gust', 'Wind Speed', 'Wind Direction', 'Sea Level Pressure', 'Cloud Cover', 'Visibility', 'Solar Radiation', 'Solar Energy','UV Index', 'Severe Risk', 'Sunrise', 'Sunset', 
            'Moon Phase', 'Conditions', 'Description','Icon', 'Stations'
        ])
        for Row in CSVText:

            if RowIndex == 0:
                FirstRow = Row
            else:
                to_append = []
                ColIndex = 0
                for Col in Row:
                    if ColIndex >= 2:
                        to_append.append(Row[ColIndex]) 
                        #print(len(to_append))
                    ColIndex += 1
                    
                df.loc[len(df)] = to_append
            RowIndex += 1

        return df
        """     stations = Stations()
                stations = stations.nearby(latitude, longitude)
                station = stations.fetch(3)
                race_date_start = datetime(2018,10,10, 9, 00)
                race_date_daily = datetime(2018,10,10)
                race_date_end = datetime(2018,10,10, 17,00)
                data = Hourly(station, start=race_date_start, end=race_date_end)
                data_daily = Daily(station, start=race_date_daily, end=race_date_daily)
                data = data.normalize()
                data = data.interpolate(9)
                data = data.aggregate('9H')
                data_daily = data_daily.normalize()
                df_daily = pd.DataFrame(data_daily.fetch().values)
                df =  pd.DataFrame(data.fetch().values)
                df[0] = df[0].fillna(df[0].mean())
                df[6] = df[6].fillna(df[6].mean())
                df[3] = df_daily[3].fillna(df_daily[3].mean()).fillna(0.0)
                df[10] = df[10].fillna(method="ffill").fillna(method="bfill")"""






