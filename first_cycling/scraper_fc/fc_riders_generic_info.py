from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import numpy as np
import pandas as pd

#provisional import from a file, afterwards will be done directly from a sql table/database
all_teams_generic_info = pd.read_csv('All_Teams_Generic_Info.csv')

# generates final df for storing the data
final = pd.DataFrame(columns=['Name','Age','Nation','No.','Points','Wins','Race days','Km','Gender','Category','Year','Team Name', 'Team Code', 'Rider Code'])
for Code in all_teams_generic_info['Team Code']:
    #import some information from the team table (year, team name, category, gender etc)
    Year = all_teams_generic_info['Year'].loc[all_teams_generic_info['Team Code']==Code].values[0]
    Team_Name = all_teams_generic_info.loc[all_teams_generic_info['Team Code']==Code]['Name'].values[0]
    Category = all_teams_generic_info.loc[all_teams_generic_info['Team Code']==Code]['Category'].values[0]
    Gender = all_teams_generic_info.loc[all_teams_generic_info['Team Code']==Code]['Gender'].values[0]

    #access url with detail of the rider in the team
    url = 'https://firstcycling.com/team.php?l='+str(Code)+'&riders=2'
    try:
        print('opening client for url '+ url)
        uclient = urlopen(url) # opens the client
        html_page = uclient.read() # drops the content to a variable
        uclient.close() # closes client
        print('client closed')
    except:
        print('url ' + url +' was not found')
        url = 'https://firstcycling.com/team.php?l='+str(Code)+'&riders=1'

    #bs4 crawls the html
    page_soup = soup(html_page, 'html.parser')

    #generates header for temp df
    table_container = page_soup.findAll("table")
    Team_Riders = table_container[1]
    Header = Team_Riders.findAll('thead')
    Header_split = Header[0].findAll('th')
    Riders_column_names = []
    for i in range(3,len(Header_split)):
        Riders_column_names.append(Header_split[i].getText())
    
    #dumps information from into list
    raw_list_of_riders_info = []
    Riders_column_names.insert(8, 'Empty')
    for row in Team_Riders.tbody.findAll('tr'):
        for info in row.findAll('td'):
            string_to_append = info.getText()
            string_to_append = string_to_append.replace("\n", "")
            raw_list_of_riders_info.append(string_to_append)
        if len(raw_list_of_riders_info) % len(Riders_column_names) != 0:
            raw_list_of_riders_info.insert(-4,'')
    
    #removes unwanted characters
    for index in range(len(raw_list_of_riders_info)):
        raw_list_of_riders_info[index]=raw_list_of_riders_info[index].replace("| Trainee", "")
        raw_list_of_riders_info[index]=raw_list_of_riders_info[index].replace("| ", "")

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
final.to_csv('All_Riders_Generic_Info.csv')
