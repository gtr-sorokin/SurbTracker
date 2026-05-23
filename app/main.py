# from dotenv import load_dotenv
import os

# load_dotenv()

from rail import get_departures
from telegram_client import send_message
from state import load_state, save_state

def build_message(trains):

    lines = [
        "🚆 Surbiton → Waterloo",
        ""
    ]

    for train in trains:

        lines.append(
            f"{train['time']} | "
            f"{train['status']} | "
            f"Platform {train['platform']}"
        )

    return "\n".join(lines)


def main():

    trains = get_departures()

    previous = load_state()

    if previous == trains:
        print(
            "No changes detected"
        )
        return

    message = build_message(
        trains
    )

    send_message(message)

    save_state(trains)

    print(
        "Telegram update sent"
    )


if __name__ == "__main__":

    API_ID = os.getenv("TRANSPORT_API_ID")
    API_KEY = os.getenv("TRANSPORT_API_KEY")

    main()