import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('../../data/clean', exist_ok=True)
os.makedirs('../../images', exist_ok=True)

print("[H3] Loading raw Monaco pit data...")
df = pd.read_csv('../../data/raw/monaco_raw.csv')
print("[DEBUG] Columns found:", list(df.columns))
print("[DEBUG] Shape:", df.shape)

# DYNAMIC COLUMN DETECTION - works with pit_in/pit_out OR in_time/out_time
time_cols = {}
if 'pit_in' in df.columns and 'pit_out' in df.columns:
    time_cols = {'in_time': 'pit_in', 'out_time': 'pit_out'}
    df = df.rename(columns={'pit_in': 'in_time', 'pit_out': 'out_time'})
    print("[H3] Renamed pit_in/out → in_time/out_time for pgAdmin")
elif 'in_time' in df.columns and 'out_time' in df.columns:
    time_cols = {'in_time': 'in_time', 'out_time': 'out_time'}
    print("[H3] Found in_time/out_time columns")
else:
    raise ValueError("No time columns found! Need pit_in/pit_out OR in_time/out_time")

# Convert to datetime
df['in_time'] = pd.to_datetime(df['in_time'])
df['out_time'] = pd.to_datetime(df['out_time'])
df = df.dropna()
print("[H3] After datetime conversion + NaN drop: {} rows".format(len(df)))

# H4: IQR Outlier Removal (pit_delta_seconds)
Q1 = df['pit_delta_seconds'].quantile(0.25)
Q3 = df['pit_delta_seconds'].quantile(0.75)
IQR = Q3 - Q1
lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
df_clean = df[(df['pit_delta_seconds'] >= lower) & (df['pit_delta_seconds'] <= upper)]

print("[H4] IQR bounds: {:.1f}s - {:.1f}s (removed {} outliers)".format(
    lower, upper, len(df) - len(df_clean)))
print("[H4] Clean pits: {}".format(len(df_clean)))

# Professional visualization
plt.style.use('default')
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Before/After histograms
df['pit_delta_seconds'].hist(ax=axes[0], bins=20, alpha=0.7, color='red')
axes[0].set_title('Before IQR Cleaning (Outliers in Red)')
axes[0].set_xlabel('Pit Delta (seconds)')
axes[0].set_ylabel('Frequency')

df_clean['pit_delta_seconds'].hist(ax=axes[1], bins=20, alpha=0.7, color='green')
axes[1].set_title('After IQR Cleaning (Clean Data)')
axes[1].set_xlabel('Pit Delta (seconds)')
axes[1].axvline(df_clean['pit_delta_seconds'].mean(), color='blue', linestyle='--', 
                label='Mean: {:.1f}s'.format(df_clean['pit_delta_seconds'].mean()))
axes[1].legend()

plt.tight_layout()
plt.savefig('../../images/DAY1_CLEANING.png', dpi=300, bbox_inches='tight')
plt.show()

# Export pgAdmin-ready TSV
df_clean.to_csv('../../data/clean/monaco_clean.tsv', sep='\t', index=False, na_rep='\\N')
print("[OK] H3-H4 COMPLETE: {} clean pits → monaco_clean.tsv".format(len(df_clean)))
print("[STATS] Range: {:.1f}s - {:.1f}s | Mean: {:.1f}s".format(
    df_clean['pit_delta_seconds'].min(),
    df_clean['pit_delta_seconds'].max(), 
    df_clean['pit_delta_seconds'].mean()
))
