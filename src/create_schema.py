import psycopg2

DB_CONFIG = {
    'host': '127.0.0.1',
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'Harshit@04',  # UPDATE THIS
    'port': 5432
}

def create_table():
    """H5a: Create EXACT pgAdmin schema"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pits (
        id INTEGER,
        session_id INTEGER NOT NULL,
        driver CHARACTER VARYING NOT NULL,
        team CHARACTER VARYING NOT NULL,
        in_time TIMESTAMP WITH TIME ZONE NOT NULL,
        out_time TIMESTAMP WITH TIME ZONE NOT NULL,
        pit_delta_seconds DOUBLE PRECISION NOT NULL
    );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("[OK] H5a: Table matches pgAdmin schema")

def create_indexes():
    """H5b: Fast ML indexes"""
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute("CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_driver ON pits(driver);")
    cur.execute("CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_session ON pits(session_id);")
    cur.execute("CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_in_time ON pits(in_time);")
    
    print("[OK] H5b: 3 indexes created")
    cur.close()
    conn.close()

# EXECUTE
create_table()
create_indexes()

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM pits;")
print("[OK] H5 COMPLETE: Schema ready | Current rows: {}".format(cur.fetchone()[0]))
cur.close()
conn.close()
