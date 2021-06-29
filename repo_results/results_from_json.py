import pandas as pd
import json
import Extract_from_json
from datetime import datetime

json_name = 'repo_results/14.json' #set new json name if necessary or list over files

EFJS = Extract_from_json.Extract_from_json(json_name)


# print(EFJS.Extract_info())
# print("********************")
# print(EFJS.Teams())
# print("********************")
# print(EFJS.Riders())
# print("********************")
# print(EFJS.Riders_Names())

# print(EFJS.Teams_Names())


#print(EFJS.Get_Riders_Teams())

print(EFJS.data['riders']['73811'])
for rider in EFJS.Riders():
    print(  EFJS.Get_Rider_Name(rider), 
            EFJS.Get_Rider_Nation_Code(rider), 
            EFJS.Get_Rider_Team_Id(rider),
            EFJS.Get_Rider_Team_Name(rider),
            EFJS.Get_Final_Result_Position(rider),
            EFJS.Get_Final_Time_Gap(rider),
            EFJS.Get_Final_Result_Time(rider),
            EFJS.Get_Stages_Results(rider),
            EFJS.Get_Stages_Gaps(rider),
            EFJS.Get_Finished_Race(rider))
 

print('time of winner:', EFJS.time_of_first)

print('number of stages:', EFJS.Get_Number_Of_Stages())