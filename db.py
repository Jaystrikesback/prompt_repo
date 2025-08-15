# db.py
import sqlite3
import os
from datetime import datetime

DB_FILE = "prompt_repo.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Create tables if they do not exist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            prompt_text TEXT NOT NULL,
            intended_use TEXT,
            llm_used TEXT,
            performance_score INTEGER,
            outcome TEXT,
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

# Helper CRUD functions
def create_user(username, password_hash):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (username, password_hash, created_at)
        VALUES (?, ?, ?)
    """, (username, password_hash, datetime.utcnow().isoformat()))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id

def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row

def insert_prompt(user_id, prompt):
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    cur.execute("""
        INSERT INTO prompts (
            user_id, prompt_text, intended_use, llm_used,
            performance_score, outcome, notes, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        prompt['prompt_text'],
        prompt.get('intended_use'),
        prompt.get('llm_used'),
        prompt.get('performance_score'),
        prompt.get('outcome'),
        prompt.get('notes'),
        now,
        now
    ))
    conn.commit()
    prompt_id = cur.lastrowid
    conn.close()
    return prompt_id

def update_prompt(prompt_id, prompt):
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    cur.execute("""
        UPDATE prompts SET
            prompt_text = ?,
            intended_use = ?,
            llm_used = ?,
            performance_score = ?,
            outcome = ?,
            notes = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        prompt['prompt_text'],
        prompt.get('intended_use'),
        prompt.get('llm_used'),
        prompt.get('performance_score'),
        prompt.get('outcome'),
        prompt.get('notes'),
        now,
        prompt_id
    ))
    conn.commit()
    conn.close()

def delete_prompt(prompt_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
    conn.commit()
    conn.close()

def get_prompts_for_user(user_id, filter_text=""):
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT * FROM prompts
        WHERE user_id = ?
        AND (
            prompt_text LIKE ?
            OR llm_used LIKE ?
            OR intended_use LIKE ?
        )
        ORDER BY updated_at DESC
    """
    like = f"%{filter_text}%"
    cur.execute(query, (user_id, like, like, like))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_prompt_by_id(prompt_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,))
    row = cur.fetchone()
    conn.close()
    return row
