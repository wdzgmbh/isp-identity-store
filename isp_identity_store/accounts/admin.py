from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)