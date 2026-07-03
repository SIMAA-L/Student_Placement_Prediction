import sqlite3

conn = sqlite3.connect("placement.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions(

id INTEGER PRIMARY KEY AUTOINCREMENT,

gender TEXT,

ssc REAL,

hsc REAL,

degree REAL,

mba REAL,

prediction TEXT,

probability REAL

)
""")

conn.commit()

conn.close()

print("Database Created Successfully")