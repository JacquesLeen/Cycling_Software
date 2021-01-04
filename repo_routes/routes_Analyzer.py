import requests
from bs4 import BeautifulSoup
import gpxpy
import matplotlib.pyplot as plt
import numpy as np

class Analyzer:
    def __init__(self, track_number = []):
        self.t_n= track_number

    def get_gpx_track(self):
        """Send request to la flamme rouge website to a specific gpx track
        
        Returns
        ------------
        The parsed URLs as a list
        """
        soup = []
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
        """
        for track in self.t_n:
            url = 'http://la-flamme-rouge.eu/maps/viewtrack/gpx/'+str(track)
            headers={'User-Agent':'Mozilla/5'}
            r = requests.get(url, allow_redirects=True,headers=headers)
            open('gpx/'+str(track)+'.gpx', 'wb').write(r.content)

    def get_data_from_gpx(self):
        """Extract stage name elevation, max elevation and distance from the text of the files
    
        Returns
        ------------
        A dictionary where the key is the stage name and the value is a list [positive_elevation_gain, max_elevation, distance]
        """
        data_race={}
        for track in self.t_n:
            file_name = 'gpx/'+str(track)+'.gpx'
            gpx_file= open(file_name, 'r')
            gpx = gpxpy.parse(gpx_file)
            name = gpx.tracks[0].name
            elev = [point.elevation for point in gpx.tracks[0].segments[0].points]
            elev_change = sum([ elev[i+1] - elev[i] for i in range(len(elev)-1) if elev[i+1] > elev[i] ])
            max_elev = max(elev)
            distance = round(gpx.length_2d()/1000,2)
            data_race[name] = [elev_change, max_elev, distance]

        return [data_race,elev]

    def is_over_1500(self)->bool:
        """
        determines whether the race got over 1500m of altitude
        """
        data = self.get_data_from_gpx()
        if list(data[0].values())[0][1] >= 1500:
            return True
        return False
    
    def is_over_1800(self)->bool:
        """
        determines whether the race got over 2000m of altitude
        """
        data = self.get_data_from_gpx()
        if list(data[0].values())[0][1] >= 1800:
            return True
        return False

    def is_over_2000(self)->bool:
        """
        determines whether the race got over 2000m of altitude
        """
        data = self.get_data_from_gpx()
        if list(data[0].values())[0][1] >= 2000:
            return True
        return False

    def get_distance(self)->float:
        """
        Returns the total distance in km

        Output
        -------------------------
        distance (float)
        """
        data = self.get_data_from_gpx()
        return list(data[0].values())[0][2]

    def get_altitude(self, distance=0)->float:
        """
        Returns the altitude of a waypoint, given file name and distance at which you wan to get the altitude
    
        Input
        ------------------------- 
        tracknumber (int) and distance (float, km)

        Output
        -------------------------
        altitude (float, m)
        """
        data = self.get_data_from_gpx(track_number=[tracknumber])
        waypoint = int( distance * len(data[1]) / list(data[0].values())[0][2])
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

        if self.get_altitude(finish) - self.get_altitude(finish -5) >=200:
            return True
        else:
            return False

    def quantile(self, percentage=0.5)->float:
        """
        takes as input the tracknumber and a percentage (between 0 and 1) and returns the amount of kms
        necessary to reach that percentage of covered elevation. Example: quantile(306106, 0.5) takes the infos
        from track number 306106 and returns the amount of km necessary to cover half of the total positive
        elevation.

        Input
        -------------------------
        percentage (float)

        Output
        -------------------------
        distance (float, km)
        """
        if (percentage <0 or percentage >1):
            print('Error usage: percentage must be between 0-1')
            return -1
        if (percentage == 0):
            return 0
        data=self.get_data_from_gpx()
        elev = data[1]
        elev_change = list(data[0].values())[0][0]
        max_elev = list(data[0].values())[0][1]
        distance = list(data[0].values())[0][2]
        temp = 0
        for i in range(len(elev)-1):
            if elev[i+1] > elev[i]:
                temp += elev[i+1] - elev[i]
                if(temp >= elev_change * percentage):
                    return round(dist/len(elev) * i,2)