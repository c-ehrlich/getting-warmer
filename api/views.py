from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .utils import *
from meteostat import Daily, Monthly


class HistoryForCurrentMonth(APIView):
    """
    Returns a JSON with the required data for comparing today's weather to the same month in past years

    output: JSON
      - location (?)
        - name
        - country
        - ?
      - weather_today
        - avg
        - min
        - max
      - weather_history (contains one object for each year)
        - year
        - avg
        - min
        - max
      - stats
        - % of searches where daily avg is higher than monthly avg for 1 year ago
        - % of searches where daily avg is higher than monthly avg for 5 years ago
        - % of searches where daily avg is higher than monthly avg for 10 years ago
        - % of searches where daily avg is higher than monthly avg for 20 years ago
        - % of searches where daily avg is higher than monthly avg for 50 years ago (if available)
    """
    def get(self, request, latitude, longitude, format=None):
        latitude = float(latitude)
        longitude = float(longitude)

        # get OpenWeatherMap daily weather for this location
        weather_today = get_daily_weather_by_coordinates(latitude, longitude)
        print(weather_today)

        # get meteostat historical weather for this location
        weather_history = get_monthly_weather_history(latitude, longitude)
        # location = get_nearest_station(lat, long)

        # location_dict = location.to_dict('records')[0]
        # location_json = location.to_json()

        # start = location_dict['monthly_start']
        # end = location_dict['monthly_end']

        # historical = Monthly(location_dict['wmo'], start, end)
        # historical = historical.fetch()

        weather_history = {}

        data = {
            # 'location': location_json,
            'weather_today': weather_today,
            'weather_history': weather_history,
            'stats': {},
        }

        return Response(data, status=status.HTTP_200_OK)

