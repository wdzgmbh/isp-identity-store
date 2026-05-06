from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import PasswordInput
from django.views.generic import UpdateView, DetailView, ListView

from accounts.forms import AccountEditForm
from accounts.models import Account
from accounts.tables import AccountTable


# Create your views here.

class AccountListView(LoginRequiredMixin, ListView):
    template_name = "accounts/account_list.html"
    model = Account

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        table = AccountTable(ctx['object_list'])
        ctx['person_table'] = table
        return ctx


class AccountDetail(LoginRequiredMixin, DetailView):
    template_name = "accounts/account_view.html"
    model = Account

class AccountEditView(LoginRequiredMixin, UpdateView):
    model = Account
    template_name = "accounts/account_edit.html"
    form_class = AccountEditForm

