import os
import yagmail
from db import init_db, get_db
from amadeus_client import search_flight

init_db()

EMAIL_TO = os.getenv("ALERT_EMAIL")
EMAIL_USER = os.getenv("SMTP_USER")
EMAIL_PASS = os.getenv("SMTP_PASS")

yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)

ORIGIN = "SCL"
DESTINATION = "YYZ"
RETURNS = ["YYZ", "YVR", "SEA"]

DATE_OUT = "2026-07-01"
DATE_BACK = "2026-07-12"

def check_prices():
    db = get_db()
    c = db.cursor()

    outbound_price = search_flight(ORIGIN, DESTINATION, DATE_OUT)
    if not outbound_price:
        return

    best = None

    for r in RETURNS:
        return_price = search_flight(r, ORIGIN, DATE_BACK)
        if not return_price:
            continue

        total = outbound_price + return_price
        route = f"SCL-YYZ / {r}-SCL"

        c.execute(
            "INSERT INTO prices(route, price) VALUES (?, ?)",
            (route, total)
        )

        if not best or total < best[1]:
            best = (route, total)

    db.commit()

    if best:
        yag.send(
            to=EMAIL_TO,
            subject="✈️ Mejor open-jaw encontrado",
            contents=f"Ruta: {best[0]}\nPrecio total: USD {best[1]}"
        )

if __name__ == "__main__":
    check_prices()
