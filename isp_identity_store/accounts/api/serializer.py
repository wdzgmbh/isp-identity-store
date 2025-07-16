from rest_framework import serializers

from accounts.models import Account


# Serializers define the API representation.
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'line_id', 'up_speed_mbit', 'down_speed_mbit']