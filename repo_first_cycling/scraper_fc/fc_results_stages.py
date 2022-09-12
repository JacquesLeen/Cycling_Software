from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import numpy as np
import pandas as pd
#provisional import from a file, afterwards will be done directly from a sql table/database
races_generic_info = pd.read_csv(r'C:\Users\yd26114\Desktop\fc\Tables\All_Races_Generic_Info.csv')

#Generate df fr stage races
print(len(races_generic_info[races_generic_info['Race Type']=='Stage Race']))
stage_races = races_generic_info[races_generic_info['Race Type']=='Stage Race']
start = 4000
end = len(stage_races)
stage_races = stage_races.iloc[start:end]
#stage_races= stage_races.sample(20)
final = pd.DataFrame(columns=['Pos','Born','Rider','Team', 'UCI','Time in Seconds', 'Gap in Seconds', 'Percentage of Winning Time','Race', 'Stage','Year', 'Gender','Category','Race Code', 'Full Code','Rider Code', 'Team Code'])
for race_table_index in range(len(stage_races)):
    #import some information from the race table (year, team name, category, gender etc)
    Code = stage_races.iloc[race_table_index]['Race Code']
    Year = stage_races.iloc[race_table_index]['Year']
    Category = stage_races.iloc[race_table_index]['CAT']
    Gender = stage_races.iloc[race_table_index]['Gender']
    Race_Name = stage_races.iloc[race_table_index]['Race']
    url = 'https://firstcycling.com/race.php?r='+str(Code)+'&y='+str(Year)+'&l=1'
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

    test = page_soup.find_all('option')
    stages_list = []
    for object in test:
        stages_list.append(object.getText())
    try:
        GC_index = stages_list.index('GC')
        stages_list = stages_list[GC_index+1:]
        stages_list_numbers = []
    except:
        print('Only gc available for this race')
    for element in stages_list:
        to_append = element.replace('ue', '00')
        stages_list_numbers.append(to_append[-2:])  
    for stage in stages_list_numbers:
        url = 'https://firstcycling.com/race.php?r='+str(Code)+'&y='+str(Year)+'&e='+stage
        try:
            print('opening client for url '+ url)
            uclient = urlopen(url) # opens the client
            html_page = uclient.read() # drops the content to a variable
            uclient.close() # closes client
            print('client closed')
        except:
            print('No information present for this stage')
        page_soup = soup(html_page, 'html.parser')
        #generates header for temp df
        table_container = page_soup.findAll("div", id='sta')
        try:
            table_container = table_container[0].findAll('table')
            Results = table_container[0]
            Header = Results.findAll('thead')
            Header_split = Header[0].findAll('th')
            Results_column_names = []
            for i in range(len(Header_split)):
                column_name_to_append = Header_split[i].getText()
                column_name_to_append = column_name_to_append.replace("\t", "")
                column_name_to_append = column_name_to_append.replace("\n", "")
                column_name_to_append = column_name_to_append.replace("\r", "")
                Results_column_names.append(column_name_to_append)
            #print(Results_column_names)
            #dumps information from into list
            raw_list_of_results_info = []
##################################################################################### NORMAL STAGE ##########################################################################################################################
            if (len(Results_column_names)!=3):
                for row in Results.tbody.findAll('tr'):
                    for info in row.findAll('td'):
                        string_to_append = info.getText()
                        string_to_append = string_to_append.replace("\t", "")
                        string_to_append = string_to_append.replace("\n", "")
                        string_to_append = string_to_append.replace("\r", "")
                        raw_list_of_results_info.append(string_to_append)
                #print(raw_list_of_results_info)
                #print(len(Results_column_names))

                list_of_results_info =[]
                for index in range(0, len(raw_list_of_results_info), len(Results_column_names)):
                    try:
                        sublist= []
                        for subindex in range(len(Results_column_names)):
                            sublist.append(raw_list_of_results_info[index+subindex])
                        list_of_results_info.append(sublist)
                    except:
                        print('empty table here')
                #print(list_of_results_info)
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
                df['Stage'] = stage
                df['Year'] = Year
                df['Gender'] = Gender
                df['Category'] = Category
                df['Race Code'] = Code
                df['Full Code'] = '-'+str(Code)+str(stage)+'-'
                df['Rider Code'] = Riders_Codes
                df['Team Code'] = Team_Codes
                final =pd.concat([final,df])
                #print(df)
##################################################################################### TEAM TIME TRIAL ##########################################################################################################################
            else:
                #print(Results)

                ttt_df = pd.DataFrame(columns=['Pos','Rider','Team','Time'])
                for index in range(0,len(Results.tbody.findAll('tr')),2):
                    temp_df = pd.DataFrame(columns=['Pos','Rider','Team','Time'])
                    team_results = []
                    rider_in_team = []
                    for info in Results.tbody.findAll('tr')[index].findAll('td'):
                        string_to_append = info.getText()
                        string_to_append = string_to_append.replace("\t", "")
                        string_to_append = string_to_append.replace("\n", "")
                        string_to_append = string_to_append.replace("\r", "")
                        team_results.append(string_to_append)
                    #print(team_results)
                    for info in Results.tbody.findAll('tr')[index+1].findAll('td'):
                        for name in info.findAll('span'):
                            string_to_append = name.getText()
                            string_to_append = string_to_append.replace("\t", "")
                            string_to_append = string_to_append.replace("\n", "")
                            string_to_append = string_to_append.replace("\r", "")
                            rider_in_team.append(string_to_append)
                    del rider_in_team[1::2]
                    #print(rider_in_team)
                    temp_df['Rider']=rider_in_team
                    temp_df['Pos'] = team_results[0]
                    temp_df['Team'] = team_results[1]
                    temp_df['Time'] = team_results[2]
                    ttt_df = pd.concat([ttt_df, temp_df])
                winner_time = ttt_df.iloc[0]['Time'].split(':')

                winner_time_seconds = 0
                for index in range(len(winner_time)):
                    try:
                        winner_time_seconds += int(winner_time[index]) * 60**(len(winner_time)-(index+1))
                    except:
                        print('No winning time')
                ttt_df['Time in Seconds'] = winner_time_seconds

                gap_in_seconds = []
                for index in range(len(ttt_df)):
                    if (ttt_df.iloc[index]['Pos'] != '01'):
                        gap = ttt_df.iloc[index]['Time'].split(' ')[-1].split(':')
                        gap_seconds = 0
                        for subindex in range(len(gap)):
                            try:
                                gap_seconds += int(gap[subindex]) * 60**(len(gap)-(subindex+1))
                            except:
                                gap_seconds = 0
                        gap_in_seconds.append(gap_seconds)
                    else:
                        gap_in_seconds.append(0)
                temp = []
                Codes= []
                Riders_Codes = []
                Team_Codes =[]
                for row in Results.tbody.findAll('tr'):
                    for info in row.findAll('a', href=True, title= True):
                        if 'rider' in info.get('href'):
                            Codes.append(info.get('href').split('=')[1].split('&')[0]) 


                ttt_df['Gap in Seconds'] = gap_in_seconds
                ttt_df['Time in Seconds'] = ttt_df['Time in Seconds']+ttt_df['Gap in Seconds']
                ttt_df['Percentage of Winning Time'] = ttt_df['Time in Seconds']/winner_time_seconds
                ttt_df.loc[ttt_df['Pos']=='DNF',['Time in Seconds', 'Gap in Seconds', 'Percentage of Winning Time']] = ['DNF', 'DNF', 'DNF'] 
                ttt_df.loc[ttt_df['Pos']=='OOT',['Time in Seconds', 'Gap in Seconds', 'Percentage of Winning Time']] = ['OOT', 'OOT', 'OOT'] 
                ttt_df.loc[ttt_df['Pos']=='DSQ',['Time in Seconds', 'Gap in Seconds', 'Percentage of Winning Time']] = ['DSQ', 'DSQ', 'DSQ']
                ttt_df.loc[ttt_df['Pos']=='DNS',['Time in Seconds', 'Gap in Seconds', 'Percentage of Winning Time']] = ['DNS', 'DNS', 'DNS']
                ttt_df['Race'] = Race_Name
                ttt_df['Stage'] = stage
                ttt_df['Year'] = Year
                ttt_df['Gender'] = Gender
                ttt_df['Category'] = Category
                ttt_df['Race Code'] = Code
                ttt_df['Full Code'] = '-'+str(Code)+str(stage)+'-'
                ttt_df['Rider Code'] = Codes
                #ttt_df['Team Code'] = Team_Codes
                final =pd.concat([final,ttt_df])
        except:
            print('no tables here')     

final.to_csv('All_Stages_Results_'+str(start)+'_to_'+str(end)+'.csv')

        

