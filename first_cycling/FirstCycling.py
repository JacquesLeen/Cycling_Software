import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

class FirstCycling:
    def __init__(self):
        self.base_url = "https://firstcycling.com/"

    def get_calendar(self, year: int, month: int, cat: str):

        if cat == 'WT':
            cat = 1
        elif cat == 'UCI':
            cat = 2
        elif cat == 'U23':
            cat = 3
        elif cat == 'Junior':
            cat = 4
        elif cat == 'Nat':
            cat = 9
        elif cat == 'WWT':
            cat = 5
        elif cat == 'WUCI':
            cat = 6
        elif cat == 'WJunior':
            cat = 7
        elif cat == 'WNat':
            cat = 9
        
        if len(str(month)) == 1:
            month = '0' + str(month)
        else:
            str(month)

        def _end_date(x):
            if len(x['dates']) > 5: 
                return x['year'] + '-' + x['dates'][9:] + '-' + x['dates'][6:8] 
            else:
                return x['year'] + '-' + x['dates'][3:5] + '-' + x['dates'][0:2]

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

        df = pd.DataFrame(data, columns=['dates', 'category', 'race_name', 'drop0', 'country', 'year', 'race_url', 'drop1', 'drop2', 'rider_url'])
        df['start_date'] = df['year'] + '-' + df['dates'].str[3:5] + '-' + df['dates'].str[0:2]
        df['end_date'] = df[['dates', 'year']].apply(_end_date, axis=1)
        df['race_id'] = df['race_url'].apply(lambda st: st[st.find("r=")+1:st.find("&")]).str.replace('=','')
        df['rider_id'] = df['rider_url'].apply(lambda st: st[st.find("r=")+1:st.find("&")] if st!=None else None).str.replace('=','')
        df['race_full_url'] = self.base_url + df['race_url']
        df.drop(columns=['dates', 'drop1', 'drop2', 'race_url', 'rider_url', 'drop0'], inplace=True)

        return df

