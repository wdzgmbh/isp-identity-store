from django.urls import reverse, reverse_lazy
from django_tables2 import Table, TemplateColumn, LinkColumn, Column

from accounts.models import Account, Session


class AccountLinkColumn(LinkColumn):
    def text_value(self, record, value):
        return str(record)

class AccountTable(Table):
    ACTIONS_COLUMN = """
        <a type="button" class="btn btn-sm btn-success" href="{% url 'accounts:detail-view' pk=record.pk %}">View</a>
        <a type="button" class="btn btn-sm btn-warning" href="{% url 'accounts:edit-view' pk=record.pk %}">Edit</a>
    """

    id = AccountLinkColumn(
        verbose_name="Account"
    )

    actions = TemplateColumn(template_code=ACTIONS_COLUMN)


    class Meta:
        model = Account
        fields = ['id', 'actions']


class SessionTable(Table):
    class Meta:
        model = Session
        fields = ['created_at', 'terminated_at', 'session_id', 'ip_address', 'ipv6_prefix', 'ipv6_pd_prefix', 'status']
