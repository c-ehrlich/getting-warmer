import json
from meteostat import Stations


def get_nearest_station(latitude, longitude, radius=None):
    """
    Gets the nearest weather station from the Meteostat API
    input: 
      * latitude coordinate (Integer or Float)
      * longitude coordinate (Integer or Float)
      * optional: radius in meters to search for a station (integer)
    output:
      * if a nearby station is found: a dictionary
        * 'wmo' (String): id (for making API requests)
        * 'name' (String): station name (human readable)
        * 'country' (String): station country code (2 letters, ISO 3166-1 alpha-2)
        * many additional fields - for refernece see https://dev.meteostat.net/python/stations.html#data-structure
      * if no station is found: None (this should only happen if the radius is too small,
        otherwise the nearest station will be returned no matter now "not near" it is)
    """
    stations = Stations()
    stations = stations.nearby(latitude, longitude, radius)
    station = stations.fetch(1)
    if not station.empty:
        # location = station.to_dict('records')[0]
        # location = station.to_json()
        # print(type(location))
        # location_json = json.dumps(location)
        # print(location_json)
        return station
    else:
        return None


def get_strings_for_month(month):
    """
    uses a regular expression to filter a list of strings in the format YYYY-MM-DD to return only the ones that have the correct month
    input: month (string - example: '09'
    """
    # return [s for s in strings if re.search(r'\d{4}-{month}-\d{2}'.format(month=month), s)]
    pass
