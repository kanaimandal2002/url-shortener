import sqlite3
from models import ShortenedURL
import string
import random
from datetime import datetime

class DB:
    def __init__(self, db_path='url_shortener.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shortened_urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                click_count INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def generate_unique_short_code(self, original_url, length=6):
        while True:
            chars = string.ascii_letters + string.digits
            short_code = ''.join(random.choice(chars) for _ in range(length))
            if not self.get_url_by_short_code(short_code):
                return short_code

    def save_url(self, shortened_url):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO shortened_urls (short_code, original_url)
            VALUES (?, ?)
        ''', (shortened_url.short_code, shortened_url.original_url))
        self.conn.commit()

    def get_url_by_short_code(self, short_code):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT short_code, original_url, created_at, click_count
            FROM shortened_urls
            WHERE short_code = ?
        ''', (short_code,))
        row = cursor.fetchone()
        if row:
            return ShortenedURL(*row)
        return None

    def increment_click_count(self, short_code):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE shortened_urls
            SET click_count = click_count + 1
            WHERE short_code = ?
        ''', (short_code,))
        self.conn.commit()

    def close(self):
        self.conn.close()
