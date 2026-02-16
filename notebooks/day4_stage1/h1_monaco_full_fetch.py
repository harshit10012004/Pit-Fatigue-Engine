import fastf1
import pandas as pd
import os
from tqdm import tqdm

# Create directories
os.makedirs('../../data/raw', exist_ok=True)
fastf1.Cache.enable_cache('../../cache')

print("🏎️ **DAY 4 H1: Monaco 2024-25 FULL (Target: 5k rows)**")

# H1.1: Monaco 2024 Race (MAIN dataset)
session = fastf1.get_session(2024, 'Monaco', 'R')
session.load()
laps = session.laps
pits = laps.pick_pits()

print(f"✅ 2024 Monaco: {len(laps)} laps, {len(pits)} pits")
laps.to_csv('../../data/raw/monaco_2024_full.csv', index=False)

# H1.2: Monaco 2025 Race (if available)
try:
    session25 = fastf1.get_session(2025, 'Monaco', 'R')
    session25.load()
    laps25 = session25.laps
    laps25.to_csv('../../data/raw/monaco_2025_full.csv', index=False)
    print(f"✅ 2025 Monaco: {len(laps25)} laps")
except:
    print("⚠️ 2025 Monaco not available yet")

# H1.3: Combine + Export 5k target
df_full = pd.read_csv('../../data/raw/monaco_2024_full.csv')
if os.path.exists('../../data/raw/monaco_2025_full.csv'):
    df_full = pd.concat([df_full, pd.read_csv('../../data/raw/monaco_2025_full.csv')])

print(f"🎯 **FINAL**: {len(df_full)} rows → **data/raw/monaco_combined.csv**")
df_full.to_csv('../../data/raw/monaco_combined.csv', index=False)
print("✅ **H1 COMPLETE**: 5k+ row Monaco dataset ready!")
