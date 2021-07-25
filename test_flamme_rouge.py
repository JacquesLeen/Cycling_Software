from repo_routes import FlammeRouge

fl = FlammeRouge.flamme_rouge(years=[2021], months=['07'])

df = fl.get_calendar()

# using stored tracks:
print(fl.get_tracks(fl.tracks[0]))

# using random track
print(fl.get_tracks(32324324))
