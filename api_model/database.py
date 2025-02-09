# database.py
import sqlite3
from datetime import datetime, timedelta

DB_NAME = "workouts.db"

# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            username TEXT,
            workout_details TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

# Add a workout entry
def log_workout(user_id, username, workout_details):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO workouts (user_id, username, workout_details, date) VALUES (?, ?, ?, ?)",
                   (user_id, username, workout_details, date))
    conn.commit()
    conn.close()

# Get workout summary for a timeframe
def get_summary(timeframe="daily"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    if timeframe == "daily":
        date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("SELECT username, COUNT(*) FROM workouts WHERE date = ? GROUP BY username", (date,))
    elif timeframe == "weekly":
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        cursor.execute("SELECT username, COUNT(*) FROM workouts WHERE date >= ? GROUP BY username", (start_date,))
    elif timeframe == "monthly":
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        cursor.execute("SELECT username, COUNT(*) FROM workouts WHERE date >= ? GROUP BY username", (start_date,))
    
    results = cursor.fetchall()
    conn.close()
    return results
