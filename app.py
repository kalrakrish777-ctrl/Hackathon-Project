# app.py
import os
import sqlite3
from datetime import datetime
from flask import (
    Flask, request, redirect, url_for, render_template_string,
    send_from_directory, flash, jsonify, make_response
)
from werkzeug.utils import secure_filename
import csv
import io
import random
import string

APP_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_DIR, "uploads")
DB_PATH = os.path.join(APP_DIR, "schoolhub.db")
ALLOWED_EXT = {"pdf", "png", "jpg", "jpeg", "txt", "zip", "docx"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = "dev-key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT NOT NULL UNIQUE,
        teacher_name TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT
    );
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assignment_id INTEGER NOT NULL,
        student_name TEXT NOT NULL,
        filename TEXT,
        content TEXT,
        timestamp TEXT,
        grade TEXT,
        feedback TEXT
    );
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        content TEXT NOT NULL,
        anonymous INTEGER DEFAULT 1,
        timestamp TEXT
    );
    """)
    conn.commit()
    conn.close()

init_db()

def gen_code(n=6):
    import random,string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route("/")
def index():
    return "SchoolHub Running"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
