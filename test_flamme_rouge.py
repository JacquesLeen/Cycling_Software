from repo_routes import FlammeRouge

fl = FlammeRouge.flamme_rouge(years=[2021], months=['07'])

df = fl.get_calendar()

for track in df['race_track']:
    print(fl.get_tracks(track))
