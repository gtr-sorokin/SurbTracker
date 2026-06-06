import requests
from datetime import datetime

from telegram_client import send_message


def get_buses(STOP_ID):
    url = f"https://api.tfl.gov.uk/StopPoint/{STOP_ID}/Arrivals"
    return requests.get(url).json()


def main_buses(STOP_ID):

    buses = get_buses(STOP_ID)

    message = "🚌 Upcoming buses:\n"

    counter = 5

    for b in buses:
        arrival = datetime.fromisoformat(
            b["expectedArrival"].replace("Z", "")
        )

        message += "%s at %02i:%02i\n" % (b['lineName'], int(arrival.hour), int(arrival.minute))
        counter -= 1
        if counter <= 0:
            break

    send_message(message)


if __name__ == "__main__":

    STOP_ID = "490013457N"
    main_buses(STOP_ID)