import os
import requests
import time

TOKEN = None
TOKEN_EXP = 0

def get_token():
    global TOKEN, TOKEN_EXP

    if TOKEN and time.time() < TOKEN_EXP:
        return TOKEN

    response = requests.post(
        "https://test.api.amadeus.com/v1/security/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": os.getenv("AMADEUS_API_KEY"),
            "client_secret": os.getenv("AMADEUS_API_SECRET")
        }
    )

    data = response.json()
    TOKEN = data["access_token"]
    TOKEN_EXP = time.time() + data["expires_in"] - 60
    return TOKEN


def search_flight(origin, destination, date, adults=1):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": adults,
        "currencyCode": "USD",
        "max": 5
    }

    r = requests.get(
        "https://test.api.amadeus.com/v2/shopping/flight-offers",
        headers=headers,
        params=params
    )

    if r.status_code != 200:
        return None

    offers = r.json().get("data", [])
    prices = [float(o["price"]["grandTotal"]) for o in offers]
    return min(prices) if prices else None
