import psycopg2
import pandas as pd
import io

DB_CONFIG = {
    'host': '127.0.0.1',
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'Harshit@04',  # UPDATE THIS
    'port': 5432
}

df = pd.read_csv('../../data/clean/monaco_clean.tsv', sep='\t')
print("[H6] Loading {} clean pits | Columns: {}".format(len(df), list(df.columns)))

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# Clean slate
cur.execute("TRUNCATE pits RESTART IDENTITY;")
conn.commit()
print("[H6] Table truncated - ready for fresh load")

# EXACT pgAdmin column order
columns = ['session_id', 'driver', 'team', 'in_time', 'out_time', 'pit_delta_seconds']
print("[H6] Using columns:", columns)

tsv_buffer = io.StringIO()
df[columns].to_csv(tsv_buffer, sep='\t', header=False, index=False, na_rep='\\N')
tsv_buffer.seek(0)

cur.copy_from(tsv_buffer, 'pits', sep='\t', columns=columns)
tsv_buffer.close()
conn.commit()

print("[H7] SUCCESS: {} rows loaded to PostgreSQL!".format(len(df)))

# FIXED ROUND() - ::numeric cast for double precision (YOUR DAY1 FIX!)
cur.execute("""
SELECT driver, COUNT(*) as stops, 
       ROUND(AVG(pit_delta_seconds)::numeric, 1) as avg_pit
FROM pits GROUP BY driver ORDER BY avg_pit LIMIT 5
""")
print("[H7] FASTEST PIT CREWS (Monaco 2024):")
for row in cur.fetchall():
    print("  {:<4} | {:>2} stops | {:>4.1f}s avg".format(row[0], row[1], row[2]))

# Final stats
cur.execute("SELECT MIN(pit_delta_seconds), MAX(pit_delta_seconds), AVG(pit_delta_seconds) FROM pits;")
min_pit, max_pit, avg_pit = cur.fetchone()
print("[STATS] Range: {:.1f}s - {:.1f}s | Overall avg: {:.1f}s".format(
    min_pit, max_pit, avg_pit))

cur.close()
conn.close()
print("[OK] DAY1 ETL COMPLETE! 72 Monaco pits live in PostgreSQL")
print("[NEXT] Check pgAdmin + git commit")
