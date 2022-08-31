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

Category_List = ['2','6']  #UCI male and female 

final = pd.DataFrame(columns=['Date','CAT', 'Race', 'Winner', 'Race Type', 'Race Code', 'Rider Code', 'Year', 'Month', 'Gender'])
for Year in Years_List:
    for Month in Months_List:
        for Category in Category_List:
            if Category=='2':
                Gender = 'Men'
            elif Category=='6':
                Gender = 'Women'
            url = 'https://firstcycling.com/race.php?y='+Year+'&t='+Category+'&m='+Month
            try:
                print('opening client for url '+ url)
                uclient = urlopen(url) # opens the client
                html_page = uclient.read() # drops the content to a variable
                uclient.close() # closes client
                print('client closed')
            except:
                print('url ' + url +' was not found')
    
            page_soup = soup(html_page, 'html.parser')
            table_container = page_soup.findAll("table")
            try:
                Races = table_container[1]
                Header = Races.findAll('thead')
                Header_split = Header[0].findAll('th')
                Races_Column_names = []
                raw_list_of_races_info = []
                for i in range(len(Header_split)):
                    Races_Column_names.append(Header_split[i].getText())
                for row in Races.tbody.findAll('tr'):
                    for info in row.findAll('td'):
                        string_to_append = info.getText()
                        string_to_append = string_to_append.replace("\t", "")
                        string_to_append = string_to_append.replace("\n", "")
                        string_to_append = string_to_append.replace("\r", "")
                        raw_list_of_races_info.append(string_to_append)
                list_of_races_info =[]
                for index in range(0, len(raw_list_of_races_info), len(Races_Column_names)):
                    try:
                        sublist= []
                        for subindex in range(len(Races_Column_names)):
                            sublist.append(raw_list_of_races_info[index+subindex])
                        list_of_races_info.append(sublist)
                    except:
                        print('empty table here')
                Codes= []
                Race_Codes = []
                Riders_Codes = []
                for info in Races.tbody.findAll('a', href=True, title= True):
                    Codes.append(info.get('href').split('=')[1].split('&')[0]) #Rider_Codes.append
                for index in range(0,len(Codes),2):
                    Race_Codes.append(Codes[index])
                    Riders_Codes.append(Codes[index+1])

                df = pd.DataFrame(list_of_races_info,columns=Races_Column_names)
                df['Race Type'] = 'One Day'
                df.loc[df['CAT'].str[:1] == '2', 'Race Type'] = 'Stage Race'
                df['Race Code']= Race_Codes
                df['Rider Code'] = Riders_Codes
                df['Year']=Year
                df['Month']=Month
                df['Gender'] = Gender

                final =pd.concat([final,df])
            except:
                print('no races for this month')
final.to_csv('All_Races_Generic_Info.csv')
