from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('monthly/<str:latitude>/<str:longitude>', views.HistoryForCurrentMonth.as_view()),
]