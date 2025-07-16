from django.contrib import admin
from django.urls import path

from radius.views import AuthHomeIdView

urlpatterns = [
    path('auth/home-id/<path:home_id>', AuthHomeIdView.as_view())
]
