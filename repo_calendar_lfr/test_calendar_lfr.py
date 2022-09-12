from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import numpy as np
import pandas as pd

# import years from 2000 to 2022 and convert as list of string for future usage
Years = np.arange(2000,2023,1)
Years_List =list(Years)
Years_List = [str(year) for year in Years_List]
# import months of the year and convert as list of string for future usage
Months = np.arange(1,13,1)
Months_List = list(Months)
Months_List =[str(month) for month in Months_List]


attach_to_df = []
for Year in Years_List:
    for Month in Months_List:
        url = r'https://www.la-flamme-rouge.eu/maps/races/calendar?month='+Month+r'&year='+Year
        try:
            print('opening client for url '+ url)
            uclient = urlopen(url) # opens the client
            html_page = uclient.read() # drops the content to a variable
            uclient.close() # closes client
            print('client closed')
        except:
            print('url ' + url +' was not found')
        page_soup = soup(html_page, 'html.parser')
        for td in page_soup.find_all('td', {"class":"day--anotherMonth"}):
            td.decompose()
        #print(page_soup)
        day_info = page_soup.findAll("td", {"class":"day"})

        for info in day_info:
            day_list = info.findAll("div", {"class":"day__header__day"})
            day = day_list[0].getText()
            day=day.replace(" ", "")
            day=day.replace("\n", "")
            date = Year + "-"+ Month + "-"+str(day)
            races_on_that_day = []
            container_exclude_day_header = info.findAll("div", {"class":"day__body"})
            races_bs4 = container_exclude_day_header[0].findAll('a', href=True)
            for i in range(len(races_bs4)):
                races_info = [date]
                href = races_bs4[i].get('href')
                if (href.startswith("/maps/viewtrack")):
                    code = href.split("/")[3].split("?")[0]
                    races_info.append(str(code))
                elif (href.startswith("/maps/races/view")):
                    code = 'xxxxxxx'
                    races_info.append(code)
                race_name = races_bs4[i].find('div', {"class":"race__name"}).getText()
                race_name=race_name.replace("  ", "")
                race_name=race_name.replace("\n", "")
                if (race_name[-1] == " "):
                    race_name= race_name[:-1]
                races_info.append(race_name)
                race_meta = races_bs4[i].find('div', {"class":"race__meta"}).getText()
                race_meta=race_meta.replace("  ", "")
                race_meta=race_meta.replace("\n", "")
                if (race_meta.startswith(" -")):
                    parcour_type = races_bs4[i].find('div', {"class":"race__meta"}).find('span').get('class')[1]
                    race_meta = parcour_type + race_meta
                else:
                    parcour_type = 'undefined'
                    race_meta = parcour_type + " - " + race_meta
                race_meta = race_meta.split(" - ")
                race_meta[-1]=race_meta[-1].replace(" -", "")
                for i in range(len(race_meta)):
                    races_info.append(race_meta[i])
                attach_to_df.append(races_info)

final = pd.DataFrame(attach_to_df,columns=['Date','Track Code', 'Race Name', 'Parcour Type', 'Class', 'Category'])

final.to_csv('LFR_Calendar_Info.csv')