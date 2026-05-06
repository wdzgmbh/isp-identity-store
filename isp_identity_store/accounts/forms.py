from django.contrib.auth.hashers import make_password
from django.forms import PasswordInput
from django.forms.models import modelform_factory, ModelForm

from accounts.models import Account

class AccountEditForm(ModelForm):
    class Meta:
        model = Account
        fields = ['line_id', 'user', 'password', 'down_speed_mbit', 'up_speed_mbit']
        widgets = {
            "password": PasswordInput
        }

    def clean(self):
        if self.cleaned_data['password'] is None:
            del self.cleaned_data['password']
        else:
            # We have to ensure, it is a hash.
            self.cleaned_data['password'] = make_password(self.cleaned_data['password'])

        super().clean()

