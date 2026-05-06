from django.contrib import admin
from django.urls import path, include

from accounts.views import AccountListView, AccountDetail, AccountEditView

app_name = 'accounts'

urlpatterns = [
    path('api/', include("accounts.api.urls")),
    path('', AccountListView.as_view(), name='list-view'),
    path('<uuid:pk>', AccountDetail.as_view(), name='detail-view'),
    path('<uuid:pk>/edit', AccountEditView.as_view(), name='edit-view'),
]
