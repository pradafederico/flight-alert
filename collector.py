import sqlite3
import random
from datetime import datetime

ROUTES = [
    "SCL → YYZ",
    "SCL → YVR",
    "SCL → SEA"
]

def insert_fake_price():
    conn = sqlite3.connect("flights.db")
    c = conn.cursor()

    route = random.choice(ROUTES)
    price = random.randint(650, 1200)

    c.execute(
        "INSERT INTO prices (route, price, timestamp) VALUES (?, ?, ?)",
        (route, price, datetime.now())
    )

    conn.commit()
    conn.close()

    print(f"Inserted {route} - ${price}")

if __name__ == "__main__":
    insert_fake_price()
