from django.contrib import admin
from django.urls import path, include

from accounts.views import AccountListView, AccountDetail

app_name = 'accounts'

urlpatterns = [
    path('api/', include("accounts.api.urls")),
    path('', AccountListView.as_view(), name='list-view'),
    path('<uuid:account_id>', AccountDetail.as_view(), name='detail-view'),
    path('<uuid:account_id>/edit', AccountDetail.as_view(), name='edit-view'),
]
