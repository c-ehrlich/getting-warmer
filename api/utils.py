from gettingwarmer.settings import OPEN_WEATHER_API_KEY
import json
from meteostat import Stations
from requests import get
from math import cos, asin, sqrt, pi


def distance_between_coordinates(lat1, lon1, lat2, lon2):
    """
    Returns the distance between two sets of coordinates (WGS84), in kilometers
    """
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...


def get_daily_weather_by_coordinates(latitude, longitude):
    """
    Connects to OpenWeatherMap API to get the current weather for a given location
    
    inputs
      - latitude coordinate (Integer or Float)
      - longitude coordinate (Integer or Float)

    output: 
      - dictionary:
        - 'avg': daily average
        - 'min': daily minimum
        - 'max': daily maximum
    """
    response = get(f'http://api.openweathermap.org/data/2.5/forecast/daily?lat={latitude}&lon={longitude}&cnt={1}&appid={OPEN_WEATHER_API_KEY}')
    response = response.json()
    weather_today = {
        'avg': kelvin_to_celsius(response['list'][0]['temp']['day']),
        'min': kelvin_to_celsius(response['list'][0]['temp']['min']),
        'max': kelvin_to_celsius(response['list'][0]['temp']['max']),
    }
    return weather_today


def does_station_have_enough_data(station):
    """
    Check if a station has enough data to use it for past weather data calculations
    And returns either 'monthly', 'daily', or 'hourly' depending on which dataset needs to be used
    """
    pass
    # if monthly start is not null 
    # and monthly end is not null 
    # and monthly start is current month 20 years ago or older
    # and monthly end is current month of last year or newer
        # return 'monthly'

    # if daily start is not null
    # and daily end is not null
    # and daily start is 1st of current month 20 years ago or older
    # and daily end is 31st of current month last year or newer
        # return 'daily'

    # if hourly start is not null
    # and hourly end is not null
    # and hourly start is 00:00 of current month 20 years ago or older
    # and hourly end is 23:00 of current month last year or newer
        # return 'hourly'

    return None
    


def get_monthly_weather_history(latitude, longitude):
    # get nearest meteostat station
    location = get_nearest_station(latitude, longitude)
    location_dict = location.to_dict('records')[0]
    # print(location_dict)

    return None


def get_nearest_station(latitude, longitude, radius=None):
    """
    Gets the nearest weather station from the Meteostat API
    input: 
      - latitude coordinate (Integer or Float)
      - longitude coordinate (Integer or Float)
      - optional: radius in meters to search for a station (integer)
    output:
      * if a nearby station is found: a dictionary
        - 'wmo' (String): id (for making API requests)
        - 'name' (String): station name (human readable)
        - 'country' (String): station country code (2 letters, ISO 3166-1 alpha-2)
        - many additional fields - for refernece see https://dev.meteostat.net/python/stations.html#data-structure
      * if no station is found: None (this should only happen if the radius is too small,
        otherwise the nearest station will be returned no matter now "not near" it is)
    """
    stations = Stations()
    stations = stations.nearby(latitude, longitude, radius)
    counter = 1

    while True:
        station = stations.fetch(counter)
        if not station.empty:
            print("station", station)
            location = station.to_dict('records')[0]
            print(f"{location['name']}, {location['country']}")
            print(f"hourly: {location['hourly_start']} - {location['hourly_end']}")
            print(f"daily: {location['daily_start']} - {location['daily_end']}")
            print(f"monthly: {location['monthly_start']} - {location['monthly_end']}")

            # calculate distance
            lat2 = float(location['latitude'])
            lon2 = float(location['longitude'])
            distance = distance_between_coordinates(latitude, longitude, lat2, lon2)
            print(f"distance: {distance}")

            print(type(location['monthly_start']))
            break
            # location = station.to_dict('station')[0]
            # print(location['monthly_start'])
            # print(location['monthly_end'])
            # location = station.to_dict('records')[0]
            # location = station.to_json()
            # print(type(location))
            # location_json = json.dumps(location)
            # print(location_json)

    return station


def get_strings_for_month(month):
    """
    uses a regular expression to filter a list of strings in the format YYYY-MM-DD to return only the ones that have the correct month
    input: month (string - example: '09'
    """
    # return [s for s in strings if re.search(r'\d{4}-{month}-\d{2}'.format(month=month), s)]
    pass


def kelvin_to_celsius(temperature):
    """
    Converts a temperature from Kelvin to Celsius
    input: temperature (Float, Int, or String)
    output: temperature (Float)
    """
    return round(float(temperature) - 273.15, 1)
