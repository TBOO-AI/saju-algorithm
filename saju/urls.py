# example/urls.py
from django.urls import path

from saju.views import index, character


urlpatterns = [
    path('me', index),
    path('character', character),
]