import sqlite3

def get_db():
    return sqlite3.connect("prices.db", check_same_thread=False)

def init_db():
    db = get_db()
    c = db.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            route TEXT,
            price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
