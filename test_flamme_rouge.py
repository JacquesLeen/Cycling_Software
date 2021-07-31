from repo_routes import FlammeRouge
import json
import pandas as pd
import difflib

# test also merge with race results
with open('race_final.json') as f:
    results = json.loads(f.read())

stage_1 = pd.DataFrame(results['Stage - stage1'])

fl = FlammeRouge.flamme_rouge(years=[2021], months=['03'])

df = fl.get_calendar()

# using stored tracks:
#print(fl.get_tracks(fl.tracks[0]))

# Catalunya stage 1
test_track, test_ele = fl.get_tracks(324148)

df['race_name_closest'] = df['race_name'].apply(lambda x: difflib.get_close_matches(x, stage_1['Race Name'])[0])
print(df['race_name_closest'])



