from django.contrib import admin
from django.urls import path, include

from radius.views import AuthHomeIdView

urlpatterns = [
    path('api/', include("accounts.api.urls"))

]
