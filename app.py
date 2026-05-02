from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import os
import uuid
from datetime import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database setup
def init_db():
    conn = sqlite3.connect('lostfound.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT DEFAULT 'found',
            finderName TEXT,
            contact TEXT,
            category TEXT,
            foundDate TEXT,
            location TEXT,
            pickupLocation TEXT,
            photo TEXT,
            status TEXT DEFAULT 'unclaimed',
            createdAt TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report-lost')
def report_lost():
    return render_template('report-lost.html')

@app.route('/submit', methods=['POST'])
def submit():
    photo_filename = None
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo and photo.filename:
            ext = photo.filename.rsplit('.', 1)[-1].lower()
            photo_filename = f"{uuid.uuid4().hex}.{ext}"
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
    
    item_type = request.form.get('type', 'found')
    pickup_location = request.form.get('pickupLocation')
    
    # If "Location Found" selected, use the exact location typed by user
    if pickup_location == 'location_found':
        location_exact = request.form.get('locationExact')
        if location_exact:
            pickup_location = location_exact
    
    # If "Last Seen" selected, use the Last Seen Location directly
    if pickup_location == 'last_seen':
        pickup_location = request.form.get('location')
    
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    data = (
        item_type,
        request.form.get('finderName'),
        request.form.get('contact'),
        request.form.get('category'),
        request.form.get('foundDate'),
        request.form.get('location'),
        pickup_location,
        photo_filename,
        'unclaimed',
        created_at
    )
    
    conn = sqlite3.connect('lostfound.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO items (type, finderName, contact, category, foundDate, location, pickupLocation, photo, status, createdAt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()
    
    if item_type == 'found':
        return render_template('success-found.html')
    else:
        return render_template('success-lost.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    item_type = request.args.get('type', '')
    date_from = request.args.get('dateFrom', '')
    date_to = request.args.get('dateTo', '')
    
    conn = sqlite3.connect('lostfound.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    sql = 'SELECT * FROM items WHERE 1=1'
    params = []
    
    if query:
        sql += ' AND (location LIKE ? OR pickupLocation LIKE ? OR finderName LIKE ?)'
        params.extend([f'%{query}%', f'%{query}%', f'%{query}%'])
    if category:
        sql += ' AND category = ?'
        params.append(category)
    if item_type:
        sql += ' AND type = ?'
        params.append(item_type)
    if date_from:
        sql += ' AND foundDate >= ?'
        params.append(date_from)
    if date_to:
        sql += ' AND foundDate <= ?'
        params.append(date_to)
    
    # Filter out claimed items from main search
    sql += ' AND status != ?'
    params.append('claimed')
    sql += ' ORDER BY createdAt DESC'
    c.execute(sql, params)
    items = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return render_template('search.html', items=items, query=query, category=category, 
                         item_type=item_type, date_from=date_from, date_to=date_to)

@app.route('/archives')
def archives():
    conn = sqlite3.connect('lostfound.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM items WHERE status = ? ORDER BY createdAt DESC', ('claimed',))
    items = [dict(row) for row in c.fetchall()]
    conn.close()
    return render_template('archives.html', items=items)

@app.route('/mark-claimed/<int:item_id>', methods=['GET', 'POST'])
def mark_claimed(item_id):
    conn = sqlite3.connect('lostfound.db')
    c = conn.cursor()
    c.execute('UPDATE items SET status = ? WHERE id = ?', ('claimed', item_id))
    conn.commit()
    conn.close()
    return render_template('success-claimed.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(basedir, 'static', 'uploads'), filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
