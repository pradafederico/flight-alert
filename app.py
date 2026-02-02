from flask import Flask, render_template_string
import sqlite3
import os
from db import init_db

app = Flask(__name__)

# 🔥 CLAVE: inicializa DB al arrancar
init_db()

@app.route("/")
def dashboard():
    conn = sqlite3.connect("flights.db")
    c = conn.cursor()
    c.execute("""
        SELECT route, price, timestamp
        FROM prices
        ORDER BY timestamp DESC
        LIMIT 100
    """)
    rows = c.fetchall()
    conn.close()

    html = """
    <h1>✈️ Flight Price Dashboard</h1>
    <table border="1" cellpadding="6">
        <tr>
            <th>Route</th>
            <th>Price</th>
            <th>Timestamp</th>
        </tr>
        {% for r in rows %}
        <tr>
            <td>{{ r[0] }}</td>
            <td>{{ r[1] }}</td>
            <td>{{ r[2] }}</td>
        </tr>
        {% endfor %}
    </table>
    """

    return render_template_string(html, rows=rows)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

from collector import insert_fake_price

@app.route("/collect")
def collect():
    result = insert_fake_price()
    return result
    


  
