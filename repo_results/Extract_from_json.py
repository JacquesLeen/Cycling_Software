from numpy import NAN, nan
import pandas as pd
import json
from datetime import datetime

class Extract_from_json:
    def __init__(self, file_Name: str) -> None:
        """Set Name of the File as Member of Class Object"""
        self.file_name = file_Name
        """Set Data of the File as Member of Class Object"""
        with open(self.file_name) as filename:
            self.data = json.load(filename)
        """Set Total Time of Winner, and Name as Members of Class Object"""
        self.time_of_first = 0
        for rider in list(self.data['riders'].keys()):
            if self.data['riders'][str(rider)].get('overall') is not None:
                if self.data['riders'][str(rider)].get('overall')['position'] == 1 :
                    self.winner_name = str(self.data['riders'][str(rider)].get('firstName')) + str(self.data['riders'][str(rider)].get('lastName'))
                    self.time_of_first = str(self.data['riders'][str(rider)].get('overall')['time'])
                    hh, mm, ss = self.time_of_first.split(':')
                    self.tof_seconds = int(hh)*3600 + int(mm)*60 + int(ss)
        """Set Number of Stages as Member Class Object"""
        self.nr_stages = self.Get_Number_Of_Stages()
        """Set List of Winning Times as Member of Class Object"""
        self.stages_winning_time = []
        for i in range(self.nr_stages):
            winning_time = str(self.Get_Time_Of_Stage_Winner(i+1))
            winning_time = datetime.strptime(winning_time, "%H:%M:%S")
            winning_time_delta = winning_time - datetime(1900,1,1)
            winning_time_seconds = winning_time_delta.total_seconds()
            self.stages_winning_time.append(winning_time_seconds)
        """Set List Of Stage Winners as Member of Class Object"""
        self.stage_winners_names = []
        for i in range(self.nr_stages):
            for rider in list(self.data['riders'].keys()):
                temp =[]
                if self.data['riders'][str(rider)].get('stage-'+ str(i+1)) is not None:
                    if self.data['riders'][str(rider)].get('stage-'+ str(i+1))['stagePosition'] == 1 :
                        temp.append(str(self.data['riders'][str(rider)].get('firstName')))
                        temp.append(str(self.data['riders'][str(rider)].get('lastName')))
                        temp.append(str(self.data['riders'][str(rider)].get('id')))
                        self.stage_winners_names.append(temp)
        


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
    
    def Get_Stages_Winners(self):
        """
        returns list with stage winners and their id
        """
        return self.stage_winners_names

#####################################################################
#                            RESULTS                                #
#####################################################################

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
        """
        Returns result of rider in a single stage
        """
        if(stage_nr < 1) or (stage_nr > self.Get_Number_Of_Stages()):
            print("enter correct number of stage")
            return nan
        temp = self.Get_All_Stages_Results(id)
        return temp[stage_nr-1]

    def Get_Single_Stage_Gap(self, id, stage_nr):
        """
        Returns gap of rider in a certain stage
        """
        if(stage_nr < 1) or (stage_nr > self.Get_Number_Of_Stages()):
            print("enter correct number of stage")
            return nan
        temp = self.Get_All_Stages_Gaps(id)
        return temp[stage_nr-1]

    def Get_Time_Of_Stage_Winner(self, stage_nr):
        """
        Returns time fo stage winner
        """
        if(stage_nr < 1) or (stage_nr > self.Get_Number_Of_Stages()):
            print("enter correct number of stage")
            return nan
        else:
            riders = self.Riders()
            for rider in riders:
                if (self.Get_Single_Stage_Result(rider, stage_nr) ==1):
                    winner = rider
                    break
            return self.data['riders'][str(winner)].get('stage-'+str(stage_nr))['stageTime']

    def Get_Percentage_Of_Winning_Time (self, id, stage_nr):
        """
        Returns % of time of single stage
        """
        if(self.Get_Single_Stage_Gap(id, stage_nr) == "dnf"):
            return "dnf"
        winning_time_seconds = self.stages_winning_time[stage_nr-1]
        rider_gap = str(self.Get_Single_Stage_Gap(id, stage_nr))
        rider_gap = datetime.strptime(rider_gap, "%H:%M:%S")
        rider_gap_delta = rider_gap - datetime(1900,1,1)
        rider_gap_seconds = rider_gap_delta.total_seconds()
        return (rider_gap_seconds + winning_time_seconds)/winning_time_seconds

    def Get_Percentage_Of_Total_Time (self, id):
        """
        Returns % of total time
        """
        if(self.Get_Final_Result_Time(id) is NAN):
            return "dnf"
        elif(self.Get_Final_Result_Position != 1):
            temp = str(self.Get_Final_Time_Gap(id))
            hh, mm, ss = temp.split(':')
            time_gap= int(hh)*3600 + int(mm)*60 + int(ss)
            return (time_gap + self.tof_seconds)/self.tof_seconds
        else:
            return 1.0

    def Get_Stage_Time(self, id, stage_nr):
        """
        returns the stage time of the rider
        """
        time_of_winner = int(self.stages_winning_time[stage_nr-1])
        if (self.Get_Single_Stage_Result(id, stage_nr) == 1):
            return time_of_winner
        elif(self.Get_Single_Stage_Result(id, stage_nr) == 'dnf'):
            return 'dnf'
        temp = str(self.Get_Single_Stage_Gap(id, stage_nr))
        hh, mm, ss = temp.split(':')
        time_gap= int(hh)*3600 + int(mm)*60 + int(ss)
        time_gap = time_gap + time_of_winner
        hh = str(time_gap // 3600)
        time_gap = time_gap - int(hh)*3600
        mm = str(time_gap // 60)
        time_gap = time_gap - int(mm) * 60
        ss = str(time_gap)
        return hh+':'+mm +':'+ ss

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