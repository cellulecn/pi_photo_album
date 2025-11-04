import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "photo_album.db")
PHOTOS_DIR = os.path.join(BASE_DIR, "photos")
THUMB_DIR = os.path.join(BASE_DIR, "static", "thumbs")

# 创建必要目录
os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(THUMB_DIR, exist_ok=True)

# 创建数据库及表
conn = sqlite3.connect(DB_PATH)
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

print("Initialization complete: directories and database table are ready.")
