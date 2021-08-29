from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .utils import *
from meteostat import Daily, Monthly


class HistoryForCurrentMonth(APIView):
    def get(self, request, lat, long, format=None):

        lat = float(lat)
        long = float(long)

        location = get_nearest_station(lat, long)



        location_dict = location.to_dict('records')[0]
        location_json = location.to_json()

        start = location_dict['monthly_start']
        end = location_dict['monthly_end']

        historical = Monthly(location_dict['wmo'], start, end)
        historical = historical.fetch()

        # print(historical)

        data = {
            'location': location,
        }

        return Response(location_json, status=status.HTTP_200_OK)


class RandomLocation(APIView):
    def get(self, request):
        return Response({'message': 'todo'}, status=status.HTTP_200_OK)
