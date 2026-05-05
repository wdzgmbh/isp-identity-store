# Routers provide an easy way of automatically determining the URL conf.
from django.urls import include, path
from rest_framework import routers

from accounts.api.views import AccountViewSet
from radius.api.views import RadiusAuthView

urlpatterns = [
    path("auth", RadiusAuthView.as_view({'post': 'post'}), name="auth"),
]