import sqlite3

def migrate():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    
    # 1. Rename existing table
    try:
        cur.execute("ALTER TABLE events RENAME TO events_old")
    except sqlite3.OperationalError:
        # Table might not exist or already renamed
        pass

    # 2. Create new table with ID
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            date TEXT
        )
    """)

    # 3. Copy data from old table if it exists
    try:
        cur.execute("INSERT INTO events (title, date) SELECT title, date FROM events_old")
        cur.execute("DROP TABLE events_old")
    except sqlite3.OperationalError:
        pass
        
    con.commit()
    con.close()
    print("Database migration completed successfully.")

if __name__ == "__main__":
    migrate()
