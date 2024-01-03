from flask import Flask, render_template, request, redirect
import sqlite3
import string
import random

app = Flask(__name__)

# Database setup
conn = sqlite3.connect('url_shortener.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        short_url TEXT NOT NULL UNIQUE
    )
''')
conn.commit()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']
    short_url = generate_short_url()

    # Store the mapping in the database
    cursor.execute('INSERT INTO urls (original_url, short_url) VALUES (?, ?)', (original_url, short_url))
    conn.commit()

    return render_template('shorten.html', short_url=short_url)

@app.route('/<short_url>')
def redirect_to_original(short_url):
    cursor.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,))
    result = cursor.fetchone()

    if result:
        original_url = result[0]
        return redirect(original_url)
    else:
        return render_template('not_found.html')

if __name__ == '__main__':
    app.run(debug=True)
