import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS events (title TEXT, date TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS registrations (name TEXT, email TEXT, event TEXT)")

con.commit()
con.close()

print("Database created successfully")
