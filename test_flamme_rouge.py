from repo_routes import flamme_rouge

fetcher = flamme_rouge.flamme_rouge(years=[2021], months=['07'])

df = fetcher.get_calendar()

total_tracks = []
for track in df['race_track']:
    total_tracks.append(fetcher.get_tracks(tracks=track))

print(total_tracks)