import fastf1
import pandas as pd
import json

fastf1.Cache.enable_cache('cache')

session = fastf1.get_session(2024, 'Monza', 'R')
session.load()

lap = session.laps.pick_drivers('VER').pick_fastest()
pos = lap.get_pos_data()
tel = lap.get_car_data()

merged = pd.merge_asof(
    pos.sort_values('Time'),
    tel[['Time', 'Brake', 'Speed']].sort_values('Time'),
    on='Time',
    direction='nearest'
)

merged['t'] = merged['Time'].dt.total_seconds()
out = merged[['t', 'X', 'Y', 'Brake', 'Speed']].to_dict(orient='records')

with open('lap.json', 'w') as f:
    json.dump(out, f)

print(f"{len(out)} points written")