# from dotenv import load_dotenv
import os

# load_dotenv()

from rail import get_departures
from telegram_client import send_message
# from state import load_state, save_state

from datetime import datetime
from zoneinfo import ZoneInfo


def build_message(trains, FROM):

    if FROM == 'SUR':
        first_line = "🚆 Surbiton → Waterloo"
    else:
        first_line = "🚆 Waterloo → Surbiton"

    lines = [
        first_line,
        ""
    ]

    for train in trains:

        lines.append(
            "%s | %s | Platform %s" % (train['time'], train['status'] if FROM == 'SUR' else train['destination'], train['platform'])
        )

    return "\n".join(lines)


def main():

    london_time = datetime.now(
        ZoneInfo("Europe/London")
    )

    FROM = 'SUR' if london_time.hour < 12 else 'WAT'

    trains = get_departures(FROM)

    message = build_message(trains, FROM)

    send_message(message)

    print("Telegram update sent")


if __name__ == "__main__":

    API_ID = os.getenv("TRANSPORT_API_ID")
    API_KEY = os.getenv("TRANSPORT_API_KEY")

    main()