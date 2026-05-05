from django.urls import reverse, reverse_lazy
from django_tables2 import Table, TemplateColumn, LinkColumn

from accounts.models import Account

class AccountLinkColumn(LinkColumn):

    def text_value(self, record, value):
        return str(record)

class AccountTable(Table):
    ACTIONS_COLUMN = """
        <a type="button" class="btn btn-sm btn-success" href="{{ record.get_absolute_url }}">View</a>
        <a type="button" class="btn btn-sm btn-warning">Edit</a>
    """

    id = AccountLinkColumn(
        verbose_name="Account"
    )

    actions = TemplateColumn(template_code=ACTIONS_COLUMN)


    class Meta:
        model = Account
        exclude = ['line_id', 'down_speed_mbit', 'up_speed_mbit']