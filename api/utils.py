from pandas._libs.tslibs import NaTType
from gettingwarmer.settings import OPEN_WEATHER_API_KEY
import json
from meteostat import Stations, Hourly, Daily, Monthly
from requests import get
from math import cos, asin, sqrt, pi
import pandas as pd
import datetime
from calendar import monthrange
import matplotlib.pyplot as plt


def distance_between_coordinates(lat1, lon1, lat2, lon2):
    """
    Returns the distance between two sets of coordinates (WGS84), in kilometers
    """
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return round(12742 * asin(sqrt(a)), 1) #2*R*asin...


def get_daily_weather_by_coordinates(latitude, longitude):
    """
    Connects to OpenWeatherMap API to get the current weather for a given location.
    
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
    Check if a station has enough data to use it for past weather data calculations (at least 20 years back)
    And returns either 'monthly', 'daily', or 'hourly' depending on which dataset needs to be used.
    If none of the data sets are sufficient, None is returned, indicating that we should find a different station

    We prefer using monthly data because it requires the least processing

    Using nested ifs because NatType and datetime objects will be changed to be noncomparable soon
    """
    now = datetime.datetime.now()
    max_start = datetime.date(now.year - 20, now.month, 1)
    min_end = datetime.date(now.year - 1, now.month, monthrange(now.year - 1, now.month)[1])

    if not (
        type(station['monthly_start']) == NaTType or
        type(station['monthly_end']) == NaTType
        ):
        if not (
            station['monthly_start'].to_pydatetime().date() > max_start or
            station['monthly_end'].to_pydatetime().date() < min_end
            ):
            return 'monthly'

    # elif not (
    #     type(station['daily_start']) == NaTType or
    #     type(station['daily_end']) == NaTType
    #     ):
    #     if not (
    #         station['daily_start'].to_pydatetime().date() > max_start or
    #         station['daily_end'].to_pydatetime().date() < min_end
    #         ):
    #         return 'daily'

    # elif not (
    #     type(station['hourly_start']) == NaTType or
    #     type(station['hourly_end']) == NaTType
    #     ):
    #     if not (
    #         station['hourly_start'].to_pydatetime().date() > max_start or
    #         station['hourly_end'].to_pydatetime().date() < min_end
    #         ):
    #         return 'hourly'

    return None
    

def get_monthly_weather_history(station):
    now = datetime.datetime.now()
    start = datetime.datetime(now.year - 20, now.month, 1)
    end = datetime.datetime(now.year - 1, now.month, monthrange(now.year - 1, now.month)[1])

    # if station['calculation_type'] == 'monthly':
    #     data = Monthly(station['id'], start, end)
    # elif station['calculation_type'] == 'daily':
    #     data = Daily(station['id'], start, end)
    # else: # station['calculation_type'] == 'hourly'
    #     data = Hourly(station['id'], start, end)

    data = Monthly(station['id'])
    data = data.fetch()
    print(f"MONTHLY - {station['id']}")
    print(data)

    # data.plot(y=['tavg', 'tmin', 'tmax'])
    # plt.show()

    # data = Daily(station['id'], start, end)
    # data = data.fetch()
    # print("DAILY")
    # print(data)

    # data = Hourly(station['id'], start, end)
    # data = data.fetch()
    # print("HOURLY")
    # print(data)

    # data = data.aggregate('1M')
    # data = data.normalize()
    # data = data.interpolate(limit = 10)
    # data = data.fetch()
    # print(data)

    return None


def get_nearest_station(latitude, longitude, counter=0):
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
    stations = stations.nearby(latitude, longitude)
    station = stations.fetch(counter + 1)
    print(station)
    location = station.to_dict('records')[counter]

    calculation_type = does_station_have_enough_data(location)
    if not calculation_type:
        return get_nearest_station(latitude, longitude, counter + 1)

    print(f"{location['name']}, {location['country']}")

    # calculate distance
    lat2 = float(location['latitude'])
    lon2 = float(location['longitude'])
    distance = distance_between_coordinates(latitude, longitude, lat2, lon2)

    location['id'] = list(station.index)[0]
    location['distance'] = distance
    location['calculation_type'] = calculation_type

    return location


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
