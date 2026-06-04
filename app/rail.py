import os
import requests

# import dotenv
# import json

from datetime import datetime
from zoneinfo import ZoneInfo

# dotenv.load_dotenv()

API_ID = os.getenv("TRANSPORT_API_ID")
API_KEY = os.getenv("TRANSPORT_API_KEY")


def load_departures_from_api(FROM):

    url = (
        f"https://transportapi.com/v3/uk/train/station/"
        f"{FROM}/live.json"
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

    # with open('%s.json' % FROM, 'w') as f:
    #     json.dump(data, f)

    all_departures = data.get("departures", {}).get("all", [])
    all_departures = [x for x in all_departures if x["mode"] == "train"]

    return all_departures


def get_departures(FROM, num=5):

    departures = []

    counter = 0

    if FROM == 'SUR':

        all_departures = load_departures_from_api(FROM)

        for train in all_departures:

            destination = train["destination_name"]

            if 'Waterloo' not in destination:
                continue

            departures.append({
                "time": train["aimed_departure_time"],
                "status": train.get("status", "Unknown"),
                "platform": train.get("platform", "?"),
                "destination": train.get("destination_name", "dest unknown"),
            })

            counter += 1

            if counter >= num:
                break
    else:

        london_time = datetime.now(
            ZoneInfo("Europe/London")
        )

        WAT_departures = load_departures_from_api(FROM)
        SUR_departures = load_departures_from_api('SUR')

        for w_train in WAT_departures:

            found_match = False
            for s_train in SUR_departures:
                if w_train['service'] == s_train['service'] or w_train['train_uid'] == s_train['train_uid']:

                    h, mins = w_train['aimed_departure_time'].split(':')

                    if london_time.hour < int(h) or (london_time.hour == int(h) and london_time.minute <= int(mins)) or (london_time.hour == 23 and int(h) == 0):
                        found_match = True
                        break


            if found_match:

                counter += 1

                departure = {
                    "time": w_train["aimed_departure_time"],
                    "status": w_train.get("status", "Unknown"),
                    "platform": w_train.get("platform", "?"),
                    "destination": w_train.get("destination_name", "dest unknown"),
                    "service": w_train.get("service", "?"),
                    "train_uid": w_train.get("train_uid", "?"),
                }

                departures.append(departure)

            if counter >= num:
                break

    return departures


if __name__ == "__main__":

    pass

    # FROM = "WAT"
    # departures = get_departures(FROM, num=5)
    # print(departures)


