import pandas as pd
import json
import Extract_from_json
from datetime import datetime

json_name = '14.json' #set new json name if necessary or list over files

EFJS = Extract_from_json.Extract_from_json(json_name)

print('time of winner:', EFJS.time_of_first)

race_dict = {}
for i in range(EFJS.Get_Number_Of_Stages()):
    Stage_DF = pd.DataFrame(columns = [
        'Race Name','Rider Name', 'Nation Code', 'Team ID',
        'Team Name',  'Stages Results', 'Stages Gaps', 
        'Percentage of Winning Time'
    ])
    for rider in EFJS.Riders():
        list_temp = []
        list_temp.append(EFJS.Get_Race_Name() + ' Stage '+ str(i+1))
        list_temp.append(EFJS.Get_Rider_Name(rider)), 
        list_temp.append(EFJS.Get_Rider_Nation_Code(rider)), 
        list_temp.append(EFJS.Get_Rider_Team_Id(rider)),
        list_temp.append(EFJS.Get_Rider_Team_Name(rider)),
        list_temp.append(EFJS.Get_Single_Stage_Result(rider, i+1)),
        list_temp.append(EFJS.Get_Single_Stage_Gap(rider, i+1 )),
        list_temp.append(EFJS.Get_Percentage_Of_Winning_Time(rider, i+1)),
        
        Stage_DF.loc[len(Stage_DF)] = list_temp 
    race_dict['stage'+str(i+1)] = Stage_DF


Overall_DF = pd.DataFrame(columns= [
    'Race Name','Rider Name', 'Nation Code', 'Team ID',
    'Team Name', 'Final Result', 'Final Time Gap','Final Result Time',
    'Finished Race', 'Total Percentage of Time'
])
for rider in EFJS.Riders():
    list_temp = []
    list_temp.append(EFJS.Get_Race_Name() + ' Overall')
    list_temp.append(EFJS.Get_Rider_Name(rider)), 
    list_temp.append(EFJS.Get_Rider_Nation_Code(rider)), 
    list_temp.append(EFJS.Get_Rider_Team_Id(rider)),
    list_temp.append(EFJS.Get_Rider_Team_Name(rider)),
    list_temp.append(EFJS.Get_Final_Result_Position(rider)),
    list_temp.append(EFJS.Get_Final_Time_Gap(rider)),
    list_temp.append(EFJS.Get_Final_Result_Time(rider)),
    list_temp.append(EFJS.Get_Finished_Race(rider)),
    list_temp.append(EFJS.Get_Percentage_Of_Total_Time(rider))
    Overall_DF.loc[len(Overall_DF)] = list_temp 
race_dict['Overall'] = Overall_DF

print(race_dict)

for i in range(EFJS.Get_Number_Of_Stages()):
    print(EFJS.Get_Time_Of_Stage_Winner(i+1))