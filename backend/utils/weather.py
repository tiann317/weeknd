import requests
import re
from backend.core.config import AUGS_LAT, AUGS_LON

url = "https://api.brightsky.dev/weather"

# https://brightsky.dev/docs/#/operations/getWeather
# https://opendata.dwd.de/climate_environment/CDC/help/stations_list_CLIMAT_data.txt
date = "2026-05-23"

# lat and lon can be passed trough Browser Geolocation API from frontend
lat = AUGS_LAT
lon = AUGS_LON


def get_wmo_id(city, stations_list):
    search = ".....;" + city
    res = "".join(re.findall(search, stations_list))
    wmo_station_id = res.replace(city, "").strip(";")
    return wmo_station_id


# TODO: shipping software with a 4.7k line txt file is not a good idea..
def get_city_wmo(city):
    with open("stations_list_CLIMAT_data.txt", "r", encoding="ISO-8859-1") as file:
        for line in file:
            if line.__contains__(city):
                return get_wmo_id(city, line)
    return -1


headers = {"Accept": "application/json"}

if __name__ == "__main__":
    city = input("City: ")

    querystring = {
        "date": date,
        "lat": lat,
        "lon": lon,
        "tz": "Europe/Berlin",
        "units": "dwd",
    }

    response = requests.get(url, headers=headers, params=querystring)
    sources = response.json().get("sources")

    try:
        for source in sources:
            print(f"Station name: {source.get('station_name')}, {date}")
            break

        weather_reports = response.json().get("weather")
        for report in weather_reports:
            res = re.findall("..:..", report.get("timestamp"))
            print(f"{res[0]}, {report.get('temperature')} C")

    except TypeError:
        print("City " + city + " is not found")
