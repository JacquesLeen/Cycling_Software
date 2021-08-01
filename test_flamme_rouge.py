from repo_routes import FlammeRouge
import json
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=1):
    """
    :param df_1: the left table to join
    :param df_2: the right table to join
    :param key1: key column of the left table
    :param key2: key column of the right table
    :param threshold: how close the matches should be to return a match, based on Levenshtein distance
    :param limit: the amount of matches that will get returned, these are sorted high to low
    :return: dataframe with boths keys and matches
    """
    s = df_2[key2].tolist()

    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))
    df_1['matches'] = m

    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2

    return df_1

# test also merge with race results
with open('race_final.json') as f:
    results = json.loads(f.read())

stage_1 = pd.DataFrame(results['Stage - stage1'])

fl = FlammeRouge.flamme_rouge(years=[2021], months=['03'])

df = fl.get_calendar()
df['race_track'] = df['race_track'].astype(int)
print(df.iloc[0])

# using stored tracks:
#print(fl.get_tracks(fl.tracks[0]))

# Catalunya stage 1
test_route_data = fl.get_tracks(324148)
route_df = pd.DataFrame.from_dict(test_route_data[0], orient='index')
route_df = route_df.reset_index().rename(columns={'index': 'race_track'})
route_df['race_track'] = route_df['race_track'].astype(int)

# merge calendar and trace
print(df.merge(route_df, on='race_track'))

# test fuzzy match race results with route data
print(fuzzy_merge(stage_1, df, 'Race Name', 'race_name', threshold=80))





