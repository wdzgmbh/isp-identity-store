from rest_framework import viewsets

from accounts.api.serializer import AccountSerializer
from accounts.models import Account


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
