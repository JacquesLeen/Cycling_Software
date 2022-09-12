import FirstCycling as FC
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import re

fc = FC.FirstCycling()

teams =fc.get_teams(year=[2022,2021], cat=['WT'])
#print(teams)
for team in teams['team_id']:
    print(fc.get_riders(team_id=str(team)))