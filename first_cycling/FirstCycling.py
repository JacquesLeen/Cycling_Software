import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

class FirstCycling:
    def __init__(self):
        self.base_url = "https://firstcycling.com/"

    def _end_date(x):
        if len(x['dates']) > 5: 
            return x['year'] + '-' + x['dates'][9:] + '-' + x['dates'][6:8] 
        else:
            return x['year'] + '-' + x['dates'][3:5] + '-' + x['dates'][0:2]

    def get_calendar(self, year: int, month: int, cat: str):

        if cat == 'WT':
            cat = 1
        elif cat == 'UCI':
            cat = 2
        elif cat == 'U23':
            cat = 3
        elif cat == 'Junior':
            cat = 4
        elif cat == 'WWT':
            cat = 5
        elif cat == 'WUCI':
            cat = 6
        elif cat == 'WJunior':
            cat = 7
        elif cat == 'Nat':
            cat = 8
        elif cat == 'WNat':
            cat = 9
        
        if len(str(month)) == 1:
            month = '0' + str(month)
        else:
            str(month)

        

        data = []
        full_url = self.base_url + f"race.php?y={str(year)}&t={str(cat)}&m={str(month)}"
        soup = BeautifulSoup(requests.get(full_url).text,'lxml')
        tables = soup.find_all('table', class_='sortTabell')
        for table in tables:
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                cols.append(row.find('img', class_='flag')['title'])
                #cols = [x for x in cols if x.startswith('rider') or x.startswith('race')]
                cols.append(str(year))
                for l in row.find_all('a'):
                    cols.append(l['href'] if (l['href'].startswith('race') and 'k=' not in l['href']) else None)
                    cols.append(l['href'] if l['href'].startswith('rider') else None)
                data.append(cols)
        try:
            df = pd.DataFrame(data, columns=['dates', 'category', 'race_name', 'drop0', 'country', 'year', 'race_url', 'drop1', 'drop2', 'rider_url'])
            df['start_date'] = df['year'] + '-' + df['dates'].str[3:5] + '-' + df['dates'].str[0:2]
            df['end_date'] = df[['dates', 'year']].apply(self._end_date, axis=1)
            df['race_id'] = df['race_url'].apply(lambda st: st[st.find("r=")+1:st.find("&")]).str.replace('=','')
            df['rider_id'] = df['rider_url'].apply(lambda st: st[st.find("r=")+1:st.find("&")] if st!=None else None).str.replace('=','')
            df['race_full_url'] = self.base_url + df['race_url']
            df.drop(columns=['dates', 'drop1', 'drop2', 'race_url', 'rider_url', 'drop0'], inplace=True)
            df.drop_duplicates(inplace=True)
            return df
        except:
            print("No race for this category in this month")
            return None


    def get_teams(self, year: list, cat: list):
        
        cats = []
        for c in cat:
            if c == 'WT':
                cats.append(1)
            elif c == 'PT':
                cats.append(2)
            elif c == 'Cont':
                cats.append(3)
            elif c == 'Amateur':
                cats.append(4)
            elif c == 'WUCI':
                cats.append(5)
            elif c == 'W-Other':
                cats.append(6)
            elif c == 'WWT':
                cats.append(7)
            elif c == 'Junior':
                cats.append(8)

        year = [str(ye) for ye in year]

        data = []
        for y in year:
            for i, c in enumerate(cats):
                full_url = self.base_url + f"team.php?d={c}&y={y}"
                soup = BeautifulSoup(requests.get(full_url).text,'lxml')
                tables = soup.find_all('table', class_='sortTabell')
                for table in tables:
                    table_body = table.find('tbody')
                    rows = table_body.find_all('tr')
                    for row in rows:
                        cols = row.find_all('td')
                        cols = [ele.text.strip() for ele in cols]
                        if len(cols) == 6:
                            cols.insert(3, '') 
                        if len(cols) == 3:
                            cols[3:3] = ['']*4
                        for l in row.find_all('a'):
                            cols.append(l['href'])
                        #cols.append(row.find('img', class_='flag')['title'])
                        cols = [x for x in cols if not x.startswith('rider')]
                        cols.append('M' if c in (1,2,3,4,8) else 'W')
                        cols.append(y)
                        cols.append(cat[i])
                        data.append(cols)

        df_teams = pd.DataFrame(data, columns=['drop', 'team', 'country', 'bike', 'wt_wins', 'uci_wins', 'uci_ranking', 'team_link', 'gender', 'year', 'category'])
        df_teams.drop(columns=['drop'], inplace=True)
        df_teams['team_url'] = 'https://firstcycling.com/' + df_teams['team_link']
        df_teams['team_id'] = df_teams['team_link'].apply(lambda st: st[st.find("l=")+1:]).str.replace('=', '')
        df_teams.drop(columns=['team_link'], inplace=True)

        return df_teams

    def get_riders(self, team_id):
        team_url = "https://firstcycling.com/team.php?l="+str(team_id)+"&riders=2"
        soup = BeautifulSoup(requests.get(team_url).text,'lxml')
        tables = soup.find_all('table', class_='sortTabell')
        for table in tables:
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            names = []
            age =[]
            nationalities=[]
            racedays =[]
            racekm=[]
            riders_id = []
    
            #get the riders' ID from the html file parsing
            riders_href =list(soup.select('a[href^="rider.php"]'))
            tags =[]
            for tag in riders_href:
                tags.append( str(tag) )
            for tag in tags:
                start = tag.find('rider.php?r=')+len('rider.php?r=')
                end = tag.find('&amp')
                riders_id.append(tag[start:end])
    
            #get riders info from the html
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                names.append(cols[0])
                age.append(cols[2])
                nationalities.append(cols[3])
                racedays.append(cols[8])
                racekm.append(cols[9])
        df_riders = pd.DataFrame(list(zip(names, age, nationalities,racedays,racekm, riders_id)),
            columns =['Name', 'Age', 'Nationality', 'Race Days', 'Race Km','ID'])
        return df_riders