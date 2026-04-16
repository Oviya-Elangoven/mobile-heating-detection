import sqlite3
from datetime import datetime

# -----------------------------
# Create DB
# -----------------------------
conn = sqlite3.connect("thermal_history.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    time TEXT,
    cpu REAL,
    temp REAL,
    charging REAL,
    fuzzy_risk REAL,
    ml_risk REAL
)
""")

conn.commit()

# -----------------------------
# Insert Data
# -----------------------------
def log_data(cpu, temp, charging, fuzzy_risk, ml_risk):

    cursor.execute("""
    INSERT INTO history
    VALUES (?,?,?,?,?,?)
    """, (
        datetime.now(),
        cpu,
        temp,
        charging,
        fuzzy_risk,
        ml_risk
    ))

    conn.commit()

# -----------------------------
# Fetch History
# -----------------------------
def get_history():

    cursor.execute("SELECT * FROM history")
    return cursor.fetchall()
