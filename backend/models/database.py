"""Database helper — thin wrapper around SQLite for the KaamDo app."""

import sqlite3
import os
from config import Config


def get_db():
    """Return a new database connection with Row factory enabled."""
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they don't exist yet."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT CHECK(role IN ('poster','worker')) NOT NULL,
            skills TEXT,
            lat REAL,
            lng REAL,
            avg_rating REAL DEFAULT 0,
            total_tasks INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            poster_id INTEGER REFERENCES users(id),
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            suggested_price_min REAL,
            suggested_price_max REAL,
            budget REAL NOT NULL,
            radius_km REAL DEFAULT 5,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            status TEXT DEFAULT 'open',
            photo_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS bids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER REFERENCES tasks(id),
            worker_id INTEGER REFERENCES users(id),
            amount REAL NOT NULL,
            message TEXT,
            match_score REAL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rater_id INTEGER REFERENCES users(id),
            ratee_id INTEGER REFERENCES users(id),
            task_id INTEGER REFERENCES tasks(id),
            score INTEGER CHECK(score BETWEEN 1 AND 5),
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()


def query_db(query, args=(), one=False):
    """Execute a SELECT query and return results as list of dicts."""
    conn = get_db()
    cursor = conn.execute(query, args)
    rows = cursor.fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    if one:
        return result[0] if result else None
    return result


def execute_db(query, args=()):
    """Execute an INSERT/UPDATE/DELETE and return lastrowid."""
    conn = get_db()
    cursor = conn.execute(query, args)
    conn.commit()
    lastrowid = cursor.lastrowid
    conn.close()
    return lastrowid
