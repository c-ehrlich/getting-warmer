from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('monthly/<str:lat>/<str:long>', views.HistoryForCurrentMonth.as_view()),
    path('random', views.RandomLocation.as_view()),
]