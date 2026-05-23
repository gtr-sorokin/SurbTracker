import os
import requests

API_ID = os.getenv("TRANSPORT_API_ID")
API_KEY = os.getenv("TRANSPORT_API_KEY")

STATION = "SUR"      # Surbiton
DESTINATION = "WAT"  # Waterloo

def get_departures():
    url = (
        f"https://transportapi.com/v3/uk/train/station/"
        f"{STATION}/live.json"
    )

    params = {
        "app_id": API_ID,
        "app_key": API_KEY,
        "darwin": "true"
    }

    response = requests.get(
        url,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    departures = []

    all_departures = data.get(
        "departures",
        {}
    ).get(
        "all",
        []
    )

    for train in all_departures:

        destination = train["destination_name"]

        if "Waterloo" not in destination:
            continue

        departures.append({
            "time": train["aimed_departure_time"],
            "status": train.get(
                "status",
                "Unknown"
            ),
            "platform": train.get(
                "platform",
                "?"
            )
        })

    return departures[:5]


if __name__ == "__main__":

    departures = get_departures()

    print(departures)


