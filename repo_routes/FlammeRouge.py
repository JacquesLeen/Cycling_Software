import requests
from bs4 import BeautifulSoup
import pandas as pd
from haversine import haversine


class flamme_rouge:
    def __init__(self, years, months):
        self.years = years
        self.months = months
        self.days = None
        self.tracks = None

    def get_calendar(self):

        race_day = []
        race_name = []
        race_track = []
        race_info = []

        if not self.years:
            print("list of years is empty")
        elif not self.months:
            print("list of months is empty")
        else:
            if not self.days:
                for year in self.years:
                    for month in self.months:
                        url = 'https://www.la-flamme-rouge.eu/maps/races/calendar?month=' + month + '&year=' + str(year)
                        headers = {'User-Agent': 'Mozilla/5'}
                        r = requests.get(url, allow_redirects=True, headers=headers)
                        soup = BeautifulSoup(r.text, 'html.parser')
                        for day in soup.find_all('td', class_='day'):
                            if len(day.attrs['class']) == 1:
                                try:
                                    day_n = day.find_all('div', class_='day__header')[0].find('div',
                                                                                              class_='day__header__day').text.strip()
                                    if int(day_n) < 10:
                                        day_n = str(year) + '-' + month + '-0' + str(day_n)
                                    else:
                                        day_n = str(year) + '-' + month + '-' + str(day_n)
                                    for a in day.find_all('a'):
                                        if 'viewtrack' in a['href']:
                                            race_track.append(a['href'].split('/')[3].split('?')[0])
                                        elif 'maps/races/view' in a['href']:
                                            race_track.append('no track available')
                                    for races in day.find_all('div', class_='day__body'):
                                        for race in races.find_all('a'):
                                            race_n = race.find('div', class_='race__name').text.replace('\n',
                                                                                                        ' - ').strip()
                                            race_info.append(
                                                race.find('div', class_='race__meta').text.replace('\n', '').replace(
                                                    '-', '').strip())
                                            race_name.append(" ".join(race_n.split()))
                                            race_day.append(day_n)
                                except:
                                    continue

        df_racedays = pd.DataFrame(
            {'date': race_day, 'race_name': race_name, 'race_info': race_info, 'race_track': race_track})
        self.tracks = race_track
        return df_racedays


    def get_tracks(self, track):
        data_race = {}
        last_point = []
        url = 'http://la-flamme-rouge.eu/maps/viewtrack/gpx/' + str(track)
        headers = {'User-Agent': 'Mozilla/5'}
        r = requests.get(url, allow_redirects=True, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        try:
            lat = []
            lon = []
            ele = []
            for i in soup.find('trkseg').find_all('trkpt'):
                lat.append(i['lat'])
                lon.append(i['lon'])
                ele.append(i.find('ele').text)
            race_name = soup.find('name').text
            elev_change = 0  ## sets elev_change = 0
            distance = 0
            max_elev = int(ele[0])  ## append last point (for weather data)
            last_point = [float(lat[-1]), float(lon[-1])]

            for i in range(1, len(ele)):  ## loops through all elements
                ## evaluate total elevation change
                if (int(float(ele[i])) > int(float(ele[i - 1]))):  ## if this point is higher than previous
                    elev_change += int(float(ele[i])) - int(float(ele[i - 1]))  ## add the difference to elev_change
                    ## search for highest point in the race
                if (int(float(ele[i])) > float(max_elev)):  ## if this point is higher than max_elev
                    max_elev = ele[i]  ## set max_elev to new value
                    ## haversine distance
                begin = (float(lat[i]), float(lon[i]))
                end = (float(lat[i - 1]), float(lon[i - 1]))
                distance += haversine(end, begin)
            ele = [int(float(x)) for x in ele]
            data_race[race_name] = [elev_change, max_elev, distance, last_point]
            #return [data_race, ele]
            return data_race, ele
        except AttributeError:
            print("No data available")
