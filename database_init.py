import sqlite3

conn = sqlite3.connect('photo_album.db')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
conn.close()
print("Database initialized.")
