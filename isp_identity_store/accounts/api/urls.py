# Routers provide an easy way of automatically determining the URL conf.
from django.urls import include, path
from rest_framework import routers

from accounts.api.views import AccountViewSet

router = routers.DefaultRouter()
router.register(r'account', AccountViewSet)


urlpatterns = [
    path('', include(router.urls)),
]