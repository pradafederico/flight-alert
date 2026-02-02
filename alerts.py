import sqlite3
import yagmail
import os

THRESHOLD = 750  # USD

def check_and_alert():
    conn = sqlite3.connect("flights.db")
    c = conn.cursor()

    c.execute("""
        SELECT route, price, timestamp
        FROM prices
        WHERE price < ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (THRESHOLD,))

    row = c.fetchone()
    conn.close()

    if not row:
        return

    route, price, ts = row

    yag = yagmail.SMTP(
        os.environ["ALERT_EMAIL"],
        os.environ["ALERT_EMAIL_PASSWORD"]
    )

    yag.send(
        to=os.environ["ALERT_TO"],
        subject="✈️ Tarifa baja detectada",
        contents=f"""
        Ruta: {route}
        Precio: USD {price}
        Fecha: {ts}
        """
    )

    print("Alert sent")

if __name__ == "__main__":
    check_and_alert()
