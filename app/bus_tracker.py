import requests
from datetime import datetime

from telegram_client import send_message


def get_buses(STOP_ID):
    url = f"https://api.tfl.gov.uk/StopPoint/{STOP_ID}/Arrivals"
    return requests.get(url).json()


def main_buses(STOP_ID):

    buses = get_buses(STOP_ID)

    counter = 5

    message_strings = []
    for b in buses:
        arrival = datetime.fromisoformat(
            b["expectedArrival"].replace("Z", "")
        )

        message_strings.append("%02i:%02i bus %s\n" % (int(arrival.hour), int(arrival.minute), b['lineName']))
        counter -= 1
        if counter <= 0:
            break

    message_strings = sorted(message_strings)

    message = "🚌 Upcoming buses:\n"
    for m in message_strings:
        message += m

    send_message(message)


if __name__ == "__main__":

    STOP_ID = "490013457N"
    main_buses(STOP_ID)