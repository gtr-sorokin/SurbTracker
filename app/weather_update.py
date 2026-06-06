import requests
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram_client import send_message


def weather_picture(code: int) -> str:
    if code == 0:
        return "☀️"
    elif code in [1, 2]:
        return "🌤"
    elif code == 3:
        return "☁️"
    elif code in [45, 48]:
        return "🌫"
    elif 51 <= code <= 57:
        return "🌦"
    elif 61 <= code <= 67:
        return "🌧"
    elif 71 <= code <= 77:
        return "🌨"
    elif 80 <= code <= 82:
        return "🌦"
    elif 85 <= code <= 86:
        return "🌨"
    elif 95 <= code <= 99:
        return "⛈"
    else:
        return "❓"


def weather_description(code: int) -> str:
    """
    Convert Open-Meteo weather code into a human-readable description.
    """

    if code == 0:
        return "Clear sky"
    elif code in [1, 2]:
        return "Mostly clear / partly cloudy"
    elif code == 3:
        return "Overcast"

    elif code in [45, 48]:
        return "Fog"

    elif 51 <= code <= 57:
        return "Drizzle"

    elif 61 <= code <= 67:
        return "Rain"

    elif 71 <= code <= 77:
        return "Snow"

    elif 80 <= code <= 82:
        return "Rain showers"

    elif 85 <= code <= 86:
        return "Snow showers"

    elif 95 <= code <= 99:
        return "Thunderstorm"

    else:
        return "Unknown weather"


def update_weather_strings():

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 51.392,
            "longitude": -0.304,
            "current": "temperature_2m,rain,weather_code",
            "hourly": "precipitation_probability",
            "forecast_days": 1,
            "timezone": "Europe/London"
        }
    )

    data = response.json()

    temperature_str = str(data["current"]["temperature_2m"]) + data['current_units']['temperature_2m']

    time_array = data['hourly']['time']
    rain_prob_array = data['hourly']['precipitation_probability']

    weather_str = weather_description(data["current"]["weather_code"])
    weather_icon = weather_picture(data["current"]["weather_code"])

    london_time = datetime.now(
        ZoneInfo("Europe/London")
    )

    for i in range(len(time_array)):
        time_array[i] = datetime.strptime(time_array[i], "%Y-%m-%dT%H:%M")

    ind = 0

    for i in range(len(time_array)):

        if london_time.day == time_array[i].day \
                and london_time.hour == time_array[i].hour:
            ind = i if london_time.minute <= 25 else min(i + 1, len(time_array)-1)
            break

    rain_prob_str = ""

    max_ind = ind + 2
    while ind <= min(max_ind, len(rain_prob_array)-1):
        rain_prob_str += "%02iH (%i%s) | " % (time_array[ind].hour, rain_prob_array[ind], '%')
        ind += 1

    rain_prob_str = rain_prob_str[:-3]

    return (temperature_str, weather_str, weather_icon, rain_prob_str)


def main_weather():

    (temperature_str, weather_str, weather_icon, rain_prob_str) = update_weather_strings()

    message = "Weather at Surbiton:\n%s: %s %s\nRain: %s\n" % (temperature_str, weather_str, weather_icon, rain_prob_str)

    # print(message)
    send_message(message)

    return


if __name__ == "__main__":

    main_weather()

