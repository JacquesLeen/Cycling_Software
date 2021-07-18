from numpy import NAN, nan
import pandas as pd
import json
from datetime import datetime

class Extract_from_json:
    def __init__(self, file_Name: str) -> None:
        self.file_name = file_Name
        with open(self.file_name) as filename:
            self.data = json.load(filename)
        self.time_of_first = 0
        for rider in list(self.data['riders'].keys()):
            if self.data['riders'][str(rider)].get('overall') is not None:
                if self.data['riders'][str(rider)].get('overall')['position'] == 1 :
                    self.time_of_first = str(self.data['riders'][str(rider)].get('overall')['time'])
                    hh, mm, ss = self.time_of_first.split(':')
                    self.tof_seconds = int(hh)*3600 + int(mm)*60 + int(ss)
    def Extract_info(self):
        return self.data['info']

    def Get_Race_Name(self):
        return self.data['info']['race']

#####################################################################
#                            TEAMS                                  #
#####################################################################

    def Teams(self):
        """
        Returns Teams IDs
        """
        return list(self.data['teams'].keys())

    def Teams_Names(self):
        """
        Returns teams names
        """
        final = []
        for team in self.Teams():
            final.append(self.data['teams'][team].get('teamName'))
        return final

#####################################################################
#                            RIDERS                                 #
#####################################################################

    def Riders(self):
        """
        Returns Riders IDs
        """
        return list(self.data['riders'].keys())

    def Riders_Names(self):
        """
        Returns Riders full names
        """
        final = []
        for rider in self.Riders():
            temp = [self.data['riders'][rider].get('firstName'), self.data['riders'][rider].get('lastName')]
            final.append(temp)
        return final
    
    def Get_Rider_Name(self, id):
        """
        returns the name of a single rider given the id
        """
        return self.data['riders'][str(id)].get('firstName') +  " " + self.data['riders'][str(id)].get('lastName')
    
    def Get_Riders_Teams(self):
        """
        return the list of teams of the riders in the race
        """
        final = []
        for rider in self.Riders():
            final.append(self.data['riders'][rider].get('teamName'))
        return final

    def Get_Rider_Nation_Code(self, id):
        """
        returns the nation code of a single rider given the id
        """
        return self.data['riders'][str(id)].get('nationCode')

    def Get_Rider_Team_Id(self, id):
        """
        returns the team id of a single rider given the id of the rider
        """        
        return self.data['riders'][str(id)].get('teamId')

    def Get_Rider_Team_Name(self, id):
        """
        returns the team name of a single rider given the id of the rider
        """        
        return self.data['riders'][str(id)].get('teamName')
    
    def Get_Finished_Race(self, id):
        """
        returns the info relative to whether the rider finished the race or not:
            output is a list with "Y/N" and a boolean for eventual further use
        """   
        if(self.data['riders'][str(id)].get('stillInTheRace') == "Y"):
            return [self.data['riders'][str(id)].get('stillInTheRace'),True]
        else:
            return [self.data['riders'][str(id)].get('stillInTheRace'),False]

    def Get_Final_Result_Position(self, id):
        """
        returns the final result (position) of the rider for that race
        """
        if (self.Get_Finished_Race(id)[1] == True):
            return self.data['riders'][str(id)].get('overall')['position']
        else:
            return NAN
    
    def Get_Final_Time_Gap(self, id):
        """
        returns the final gap in time of the rider for that race or the total time for the winner
        """
        if (self.Get_Finished_Race(id)[1] == True):
            return self.data['riders'][str(id)].get('overall')['time']
        else:
            return NAN

    def Get_Final_Result_Time(self, id):
        """
        returns the final total time of the rider
        """
        if (self.Get_Finished_Race(id)[1] == True):
            if(self.data['riders'][str(id)].get('overall')['position'] == 1):
                return self.time_of_first
            else:
                temp = str(self.Get_Final_Time_Gap(id))
                hh, mm, ss = temp.split(':')
                time_gap= int(hh)*3600 + int(mm)*60 + int(ss)
                time_gap = time_gap + self.tof_seconds 
                hh = str(time_gap // 3600)
                time_gap = time_gap - int(hh)*3600
                mm = str(time_gap // 60)
                time_gap = time_gap - int(mm) * 60
                ss = str(time_gap)
                return hh+':'+mm +':'+ ss
        else:
            return NAN

    def Get_Number_Of_Stages (self):
        """
        returns the number of stages in that event
        """
        info_list = list(pd.DataFrame(self.data['riders']).transpose().columns)
        stages = 0 
        for i in info_list:
            if 'stage' in i:
                stages = stages +1
        return stages

    def Get_All_Stages_Results (self, id):
        """
        returns partial results for the rider
        """ 
        stages = self.Get_Number_Of_Stages()
        results_list = []
        for i in range(1,stages+1):
            if ("stage-"+str(i) in self.data['riders'][str(id)] and self.data['riders'][str(id)].get('stage-'+str(i))['stagePosition'] <900):
                results_list.append(self.data['riders'][str(id)].get('stage-'+str(i))['stagePosition'])
            else:
                results_list.append('dnf')
        return results_list

    def Get_All_Stages_Gaps (self, id):
        """
        returns the time gap from the winner for every stage
        """
        stages = self.Get_Number_Of_Stages()
        results_list = []
        for i in range(1,stages+1):
            if ("stage-"+str(i) in self.data['riders'][str(id)] and 
                self.data['riders'][str(id)].get('stage-'+str(i))['stagePosition'] <900 and 
                self.data['riders'][str(id)].get('stage-'+str(i))['stagePosition'] != 1):
                results_list.append(self.data['riders'][str(id)].get('stage-'+str(i))['stageTime'])
            elif("stage-"+str(i) in self.data['riders'][str(id)] and 
                self.data['riders'][str(id)].get('stage-'+str(i))['stagePosition'] == 1):
                results_list.append('00:00:00')
            else:
                results_list.append('dnf')
        return results_list

    def Get_Single_Stage_Result(self, id, stage_nr):
        if(stage_nr < 1) or (stage_nr > self.Get_Number_Of_Stages()):
            print("enter correct number of stage")
            return nan
        temp = self.Get_All_Stages_Results(id)
        return temp[stage_nr-1]

"""
with open(json_name) as json_file:
    data = json.load(json_file)

# tira fuori tutti i risultati di ogni tappa e generali
stages_df = pd.DataFrame()
for k0 in data['riders'].keys():                        #for loop over the rider's id -> that means for every rider
    for k in data['riders'][k0].keys():                 #for loop over the results and other feature of the rider -> for every feature of that rider
        if 'stage' in k:                                # if the word stage is a part of one of those features
            for k1 in data['riders']['2313'][k].keys(): # loop over the features of the rider with id 2313 -> stage position, overall position, stage time and overall time 
                temp = pd.DataFrame.from_dict(data['riders'][k0][k], orient='index').T  # create a temporary dataframe with stage position overall position, stage time and overal time
                temp['stage'] = k   #add column for number of the stage
                temp['id'] = k0 #add column for rider id
                stages_df = stages_df.append(temp) # append this element to the main df
                stages_df.drop_duplicates(inplace=True) # drop duplicates
"""