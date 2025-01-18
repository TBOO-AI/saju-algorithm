# example/urls.py
from django.urls import path

from saju.views import saju


urlpatterns = [
    path('', saju),
]