# example/urls.py
from django.urls import path

from saju.views import saju, saju_calendar


urlpatterns = [
    path('', saju),
    path('calendar', saju_calendar),
]