# Routers provide an easy way of automatically determining the URL conf.
from django.urls import include, path
from rest_framework import routers

from accounts.api.views import AccountViewSet
from radius.api.views import RadiusAuthenticateView, RadiusAuthorizeView, RadiusAccountingView

urlpatterns = [
    path("authorize", RadiusAuthorizeView.as_view({'post': 'post'}), name="authorize"),
    path("accounting", RadiusAccountingView.as_view({'post': 'post'}), name="accounting"),
    path("authenticate", RadiusAuthenticateView.as_view({'post': 'post'}), name="authenticate"),
]