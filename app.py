from flask import Flask, render_template
from db import get_db

app = Flask(__name__)

@app.route("/")
def dashboard():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT route, price, timestamp FROM prices ORDER BY timestamp DESC LIMIT 100")
    rows = c.fetchall()
    return render_template("dashboard.html", data=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
  
