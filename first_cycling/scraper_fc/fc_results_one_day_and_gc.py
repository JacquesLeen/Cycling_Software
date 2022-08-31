from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import numpy as np
import pandas as pd

#provisional import from a file, afterwards will be done directly from a sql table/database
races_generic_info = pd.read_csv('All_Races_Generic_Info.csv')
# generates final df for storing the data
final = pd.DataFrame(columns=['Pos', 'Rider','Born','Team','Time','Time in Seconds', 'Gap in Seconds','Percentage of Winning Time','Race','Year','Gender','Category' ,'Race Code','Rider Code','Team Code'])

for race_table_index in range(len(races_generic_info)):
    #import some information from the race table (year, team name, category, gender etc)
    Code = races_generic_info.iloc[race_table_index]['Race Code']
    Year = races_generic_info.iloc[race_table_index]['Year']
    Category = races_generic_info.iloc[race_table_index]['CAT']
    Gender = races_generic_info.iloc[race_table_index]['Gender']
    Race_Name = races_generic_info.iloc[race_table_index]['Race']

    #access url with detail of the race (results)
    url =  'https://firstcycling.com/race.php?r='+str(Code)+'&y='+str(Year)+'&l=1'
    try:
        print('opening client for url '+ url)
        uclient = urlopen(url) # opens the client
        html_page = uclient.read() # drops the content to a variable
        uclient.close() # closes client
        print('client closed')
    except:
        print('url ' + url +' was not found')

    #bs4 crawls the html
    page_soup = soup(html_page, 'html.parser')

    #generates header for temp df
    table_container = page_soup.findAll("table")
    try:
        Results = table_container[3]
        Header = Results.findAll('thead')
        Header_split = Header[0].findAll('th')
        Results_column_names = []
        for i in range(len(Header_split)):
            column_name_to_append = Header_split[i].getText()
            column_name_to_append = column_name_to_append.replace("\t", "")
            column_name_to_append = column_name_to_append.replace("\n", "")
            column_name_to_append = column_name_to_append.replace("\r", "")
            Results_column_names.append(column_name_to_append)

        #dumps information from into list
        raw_list_of_results_info = []

        for row in Results.tbody.findAll('tr'):
            for info in row.findAll('td'):
                string_to_append = info.getText()
                string_to_append = string_to_append.replace("\t", "")
                string_to_append = string_to_append.replace("\n", "")
                string_to_append = string_to_append.replace("\r", "")
                raw_list_of_results_info.append(string_to_append)

        list_of_results_info =[]
        for index in range(0, len(raw_list_of_results_info), len(Results_column_names)):
            try:
                sublist= []
                for subindex in range(len(Results_column_names)):
                    sublist.append(raw_list_of_results_info[index+subindex])
                list_of_results_info.append(sublist)
            except:
                print('empty table here')
        temp = []
        Codes= []
        Riders_Codes = []
        Team_Codes =[]
        for row in Results.tbody.findAll('tr'):
            counter = 0
            for info in row.findAll('a', href=True, title= True):
                counter+=1
                Codes.append(info.get('href').split('=')[1].split('&')[0]) 
            if(counter == 1):
                Codes.append(000000)
        for index in range(0,len(Codes),2):
            Riders_Codes.append(Codes[index])
            Team_Codes.append(Codes[index+1])

        #dumps info to temp df and reorganizes        
        df = pd.DataFrame(list_of_results_info,columns=Results_column_names)

        winner_time = df.iloc[0]['Time'].split(':')

        winner_time_seconds = 0
        for index in range(len(winner_time)):
            try:
                winner_time_seconds += int(winner_time[index]) * 60**(len(winner_time)-(index+1))
            except:
                print('No winning time')
        df['Time in Seconds'] = winner_time_seconds
        df['Gap in Seconds'] = 0
        for index in range(1,len(df)):
            gap = df.iloc[index]['Time'].split(' ')[-1].split(':')
            gap_seconds = 0
            for subindex in range(len(gap)):
                try:
                    gap_seconds += int(gap[subindex]) * 60**(len(gap)-(subindex+1))
                except:
                    gap_seconds = 0
            df.at[index,'Gap in Seconds'] = gap_seconds
        df['Time in Seconds'] = df['Time in Seconds']+df['Gap in Seconds']
        df['Percentage of Winning Time'] = df['Time in Seconds']/winner_time_seconds
        df.loc[df['Pos']=='DNF',['Time in Seconds', 'Gap in Seconds', 'Percentage of Winning Time']] = ['DNF', 'DNF', 'DNF'] 
        df.loc[df['Pos']=='OOT',['Time in Seconds', 'Gap in Seconds', 'Percentage of Winning Time']] = ['OOT', 'OOT', 'OOT'] 
        df.loc[df['Pos']=='DSQ',['Time in Seconds', 'Gap in Seconds', 'Percentage of Winning Time']] = ['DSQ', 'DSQ', 'DSQ']
        df.loc[df['Pos']=='DNS',['Time in Seconds', 'Gap in Seconds', 'Percentage of Winning Time']] = ['DNS', 'DNS', 'DNS']
        df['Race'] = Race_Name
        df['Year'] = Year
        df['Gender'] = Gender
        df['Category'] = Category
        df['Race Code'] = Code
        df['Rider Code'] = Riders_Codes
        df['Team Code'] = Team_Codes

        final =pd.concat([final,df])
    except:
        print('No tables here')

final.to_csv('All_Races_Results_Info.csv')

"""

    #gets rider codes 
    Rider_Codes= []
    for info in Team_Riders.tbody.findAll('a', href=True, title= True):
            Rider_Codes.append(info.get('href').split('=')[1].split('&')[0])

    #puts info into structured list
    list_of_riders_info =[]
    for index in range(0, len(raw_list_of_riders_info), len(Riders_column_names)):
        try:
            sublist= []
            for subindex in range(len(Riders_column_names)):
                sublist.append(raw_list_of_riders_info[index+subindex])
            list_of_riders_info.append(sublist)
        except:
            print('empty table here')

    #dumps info to temp df and reorganizes        
    df = pd.DataFrame(list_of_riders_info,columns=Riders_column_names)
    df.drop(['Wins', 'Strengths'],axis=1, inplace=True)
    df.rename(columns = {'Race days':'Wins', 'Empty':'Race days'}, inplace = True)
    df['Gender'] = Gender
    df['Category'] = Category
    df['Year'] = Year
    df['Team Name']= Team_Name
    df['Team Code']= Code
    df['Rider Code']= Rider_Codes


    #concat between temp df and final
    final =pd.concat([final,df])

#generates file
"""