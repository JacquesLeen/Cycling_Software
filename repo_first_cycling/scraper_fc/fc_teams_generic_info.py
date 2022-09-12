from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import numpy as np
import pandas as pd
# import from https://firstcycling.com/

# import years frok 2000 to 2022 and convert as list of string for future usage
Years = np.arange(2000,2023,1)
Years_List =list(Years)
Years_List = [str(year) for year in Years_List]
#Years_List = ['2000','2022']

#import category codes for the teams 1 = Men WT; 2= Men Pro; 3 = Men Continental; 5 = Women UCI; 6= Women Other; 7 = Women WT; 8= Men Junior
Categories_Codes_List = ['1','2','3','5','6','7','8']

#creation of df for dumping of final results
final = pd.DataFrame(columns=['Name','Nation','Bikes', 'UCI Ranking', 'Gender', 'Category', 'Year', 'Team Code'])
for Year in Years_List:
    for Category_Code in Categories_Codes_List:

        #generates the url to crawl
        url = 'https://firstcycling.com/team.php?d='+Category_Code+'&y='+Year
        try:
            # extracts the html
            print('opening client for url '+ url)
            uclient = urlopen(url) # opens the client
            html_page = uclient.read() # drops the content to a variable
            uclient.close() # closes client
            print('client closed')
        except:
            print('url ' + url +' was not found')
        
        #bs crawls the html and extracts gender and category
        page_soup = soup(html_page, 'html.parser')
        gender= page_soup.find_all(class_="valgt")[1].getText()
        category = page_soup.find_all('option', selected=True)[0].getText()

        #creates column names with appropriate naming from the html table 
        table_container = page_soup.findAll("table")
        Teams = table_container[1]
        Header = Teams.findAll('thead')
        Header_split = Header[0].findAll('th')
        Teams_DF_column_names = []
        for i in range(1,len(Header_split)):
            Teams_DF_column_names.append(Header_split[i].getText())
        
        #extracts info and appends them into list 
        raw_list_of_teams_info = []
        Team_codes = []
        for info in Teams.tbody.findAll('td'):
            string_to_append = info.getText()
            string_to_append = string_to_append.replace("\n", "")
            raw_list_of_teams_info.append(string_to_append)
        Teams_DF_column_names.insert(0, 'Empty')

        #extracts team codes
        for info in Teams.tbody.findAll('a', href=True, title= True):
            Team_codes.append(info.get('href').split('=')[1])
        
        #generates formated list with info
        list_of_team_info =[]
        for index in range(0, len(raw_list_of_teams_info), len(Teams_DF_column_names)):
            try:
                sublist= []
                for subindex in range(len(Teams_DF_column_names)):
                    sublist.append(raw_list_of_teams_info[index+subindex])
                list_of_team_info.append(sublist)
            except:
                print('empty table here')
        
        #dumps list to temp df and fills non present info
        df = pd.DataFrame(list_of_team_info,columns=Teams_DF_column_names)
        if 'UCI Ranking' not in df.columns:
            df['UCI Ranking'] = "-"
        else:
            df['UCI Ranking'].fillna("-")

        if 'Bikes' not in df.columns:
            df['Bikes'] = "-"
        else:
            df['Bikes'].fillna("-")
        df.drop('Empty',axis=1, inplace=True)
        df['Gender'] = gender
        df['Category'] = category
        df['Year'] = Year
        df['Team Code']= Team_codes

        #concat temp df to final df
        final =pd.concat([final,df])
print(len(final))

#drops duplicate entries
final.drop_duplicates(inplace=True)
print(len(final))

#generates file
final.to_csv('All_Teams_Generic_Info.csv')