from django.contrib import admin
from django.urls import path, include

from radius.views import AuthLineIdView

urlpatterns = [
    path('api/', include("accounts.api.urls"))

]
