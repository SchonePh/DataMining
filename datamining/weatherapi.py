import requests
import json
from datetime import datetime, timedelta
import pandas as pd

weather = requests.get("https://api.weatherapi.com/v1/current.json", params={"key": "496fb0120cc847e6811113824241004", "q": "London"})
weather_json = json.loads(weather.text)
print(weather_json.get("current").get("temp_c"))

def data_cleanup(weather_json, wtype):
    columns = ["date", "max_temp", "min_temp", "avg_temp", "total_precipitation", "type"]
    days = weather_json.get("forecast").get("forecastday")
    api_data = []
    for idx, day in enumerate(days):
        if (wtype == "history"):
            length = len(days)-1
        else:
            length = len(days)
        if (idx != length):
            day_json = day.get("day")
            api_data.append([str(day.get("date")), str(day_json["maxtemp_c"]), str(day_json["mintemp_c"]), str(day_json["avgtemp_c"]), str(day_json["totalprecip_mm"]), str(wtype)])

    dm = pd.DataFrame(api_data, columns=columns)
    return dm


def get_weather_data(location, wtype, interval, apikey):

    if (wtype == "forecast"):
        weather = requests.get("https://api.weatherapi.com/v1/{}.json".format(wtype), params={"key": apikey, "q": location, "days": interval})
        weather_json = json.loads(weather.text)
        return data_cleanup(weather_json, wtype)
    
    elif (wtype == "history"):
        date = (datetime.today()).strftime('%Y-%m-%d')
        past_date =  (datetime.today() - timedelta(days=interval)).strftime('%Y-%m-%d')
        
        weather = requests.get("https://api.weatherapi.com/v1/{}.json".format(wtype), params={"key": apikey, "q": location, "dt": str(past_date), "end_dt": str(date)})
        weather_json = json.loads(weather.text)
        return data_cleanup(weather_json, wtype)
        


print(get_weather_data("London", "forecast", 3, "496fb0120cc847e6811113824241004"))