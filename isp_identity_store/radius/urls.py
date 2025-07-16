from django.contrib import admin
from django.urls import path

from radius.views import AuthLineIdView

urlpatterns = [
    path('auth/line-id/<path:line_id>', AuthLineIdView.as_view())
]
