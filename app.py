from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3, os
from PIL import Image

app = Flask(__name__)
PHOTO_DIR = os.path.join(os.getcwd(), "photos")
THUMB_DIR = os.path.join(os.getcwd(), "static", "thumbs")
os.makedirs(THUMB_DIR, exist_ok=True)

def get_db():
    conn = sqlite3.connect("photo_album.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    photos = conn.execute("SELECT * FROM photos ORDER BY upload_time DESC").fetchall()
    conn.close()
    return render_template('index.html', photos=photos)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(PHOTO_DIR, file.filename)
        file.save(path)
        img = Image.open(path)
        img.thumbnail((200, 200))
        img.save(os.path.join(THUMB_DIR, file.filename))
        conn = get_db()
        conn.execute("INSERT INTO photos (filename) VALUES (?)", (file.filename,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:photo_id>')
def delete(photo_id):
    conn = get_db()
    photo = conn.execute("SELECT filename FROM photos WHERE id=?", (photo_id,)).fetchone()
    if photo:
        os.remove(os.path.join(PHOTO_DIR, photo["filename"]))
        os.remove(os.path.join(THUMB_DIR, photo["filename"]))
        conn.execute("DELETE FROM photos WHERE id=?", (photo_id,))
        conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/photos/<path:filename>')
def photos(filename):
    return send_from_directory(PHOTO_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
