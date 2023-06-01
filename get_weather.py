# Joe McPhail
# 5/30/23
import requests

def sky_forecast(coords="38.02,-122.55"):
    api_key = "46d9324a18854b9e9b9225503233005"
    full_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={coords}&days=1&aqi=no&alerts=no"
    response = requests.get(full_url).json()
    # time_called = response['location']['localtime'][-5::]
    # print(f"API called at {time_called}")  # DONT LEAVE THIS IN (or do ?)

    tonight = {}  # big dict for everything

    forecast = response["forecast"]['forecastday'][0]  # gets into the shit we actually care about
    # non hourly
    # tonight["location"] = response['location']['name']  (only really for debug purposes to verify passed location with pulled location)
    tonight['High'] = forecast['day']['maxtemp_f']
    tonight['Low'] = forecast['day']['mintemp_f']
    tonight['Moonrise'] = forecast['astro']['moonrise']
    # tonight['moonset'] = forecast['astro']['moonset']    #### May be used later to determine if moon will actally be up when stargazing ####
    # if forecast['astro']['is_moon_up'] == 1:
        # tonight['moon_up'] = True  # 0 or 1
    # else:
        # tonight['moon_up'] = False
    tonight['Moon Illumination'] = forecast['astro']['moon_illumination']
    tonight['Sunset'] = forecast['astro']['sunset']

    # hourly
    api_hourly = forecast['hour']  # hourly part of api response
    hourly = {}

    for i in api_hourly:  # reformats condition, cloud vis, vis, and temp to hourly{}
        hour_twodigit = int(i["time"][-5:-3])  # formats hours to be restricted to a domain (8pm to midnight)
        if hour_twodigit >= 20:
            hourly[hour_twodigit] = {"condition": i["condition"]["text"],
                                    "cloud": i['cloud'], 
                                    "vis": i["vis_miles"],
                                    "temp": i['temp_f']}
    tonight['hourly'] = hourly
    return tonight