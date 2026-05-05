from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from accounts.models import Account
from accounts.tables import AccountTable


# Create your views here.

class AccountListView(TemplateView):
    template_name = "accounts/account_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        table = AccountTable(Account.objects.all())
        ctx['person_table'] = table
        return ctx


class AccountDetail(TemplateView):
    template_name = "accounts/account_view.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        account = get_object_or_404(Account, id=kwargs['account_id'])
        ctx['account'] = account
        return ctx
