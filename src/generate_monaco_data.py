import pandas as pd
import numpy as np
from datetime import datetime, timedelta
np.random.seed(42)

driver_teams = {
    'LEC': 'Ferrari', 'VER': 'RedBull', 'NOR': 'McLaren', 'HAM': 'Mercedes', 
    'SAI': 'Ferrari', 'PER': 'RedBull', 'PIA': 'McLaren', 'ALO': 'AstonMartin',
    'RUS': 'Mercedes', 'TSU': 'AlphaTauri'
}

data = []
base_time = datetime(2024, 5, 26, 15, 0)
for i in range(72):
    driver = np.random.choice(list(driver_teams.keys()))
    in_time = base_time + timedelta(minutes=np.random.uniform(60, 180))
    pit_delta = np.clip(np.random.normal(23.3, 2.5), 19, 30)
    out_time = in_time + timedelta(seconds=pit_delta)
    
    data.append({
        'id': i+1,
        'session_id': 1, 
        'driver': driver, 
        'team': driver_teams[driver],
        'in_time': in_time, 
        'out_time': out_time, 
        'pit_delta_seconds': pit_delta
    })

df = pd.DataFrame(data)
df.to_csv('../data/raw/monaco_raw.csv', index=False)
print("[OK] H2 COMPLETE: {} pits with in_time/out_time".format(len(df)))
print("Sample:")
print(df[['driver', 'team', 'in_time', 'out_time', 'pit_delta_seconds']].head())
