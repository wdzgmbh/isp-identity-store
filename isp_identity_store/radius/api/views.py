import codecs
from django.contrib.auth.hashers import check_password

from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin, ModelViewSet, ViewSet

from accounts.models import Account


class RadiusAuthView(ViewSet):

    # FIXME: We should auth this viewset somehow.
    def check_permissions(self, request):
        return True

    def _get_value_from_request(self, request, key, default=None):
        if key not in request.data:
            return default

        v = request.data[key]
        value = v['value'][0]
        if v['type'] == 'octets':
            return codecs.decode(value[2:], 'hex').decode('utf-8')

        return value

    def post(self, request, format=None):

        Framed_Protocol = self._get_value_from_request(request, "Framed-Protocol")

        if Framed_Protocol:
            User_Name = self._get_value_from_request(request, "User-Name")
            User_Password = self._get_value_from_request(request, "User-Password")
            account = Account.objects.filter(user=User_Name).first()

            if not check_password(User_Password, account.password):
                return JsonResponse(status=401, data={"Reply-Message": "Password is not valid"})

        else:
            ADSL_Agent_Circuit_Id = self._get_value_from_request(request, 'ADSL-Agent-Circuit-Id')
            account = Account.objects.filter(line_id=ADSL_Agent_Circuit_Id).first()


        if not account:
            return JsonResponse(status=401, data={"Reply-Message": "LineID is not valid"})

        # Example Values:
        #
        # Subscriber-Id: 72339069014638599
        #     Interface: ifp-0/1/7
        #     Outer VLAN: 2711
        #     IFL: ppp-0/1/7/72339069014638599
        #     Profile: default-qos-profile-pppoe
        #     Dynamic Ingress Policer Level 1:
        #         CIR: 11760000 kbps CBS: 120000 kbits
        #         PIR: 11760000 kbps PBS: 120000 kbits
        #     Dynamic Ingress Policer Level 2:
        #         CIR: 0 kbps CBS: 120000 kbits
        #         PIR: 0 kbps PBS: 120000 kbits
        #     Dynamic Ingress Policer Level 3:
        #         CIR: 0 kbps CBS: 120000 kbits
        #         PIR: 0 kbps PBS: 120000 kbits
        #     Dynamic Ingress Policer Level 4:
        #         CIR: 0 kbps CBS: 120000 kbits
        #         PIR: 0 kbps PBS: 120000 kbits
        #     Dynamic Shaper: ACCESS_SHAPER
        #         Rate Low: 11760000 kbps
        #         Rate High: 10800000 kbps
        #     Dynamic Queue: Q0_PPPOE
        #         Size: 6144000 byte

        radiusAttribute = dict()

        if account.down_speed_mbit:
            # Set the queue size to 4 ms of the shaped bandwidth
            queueSizeBytes = round((account.down_speed_mbit * 1000) * 1024 / 8 * 0.004)
            radiusAttribute["RtBrick-QoS-Queues"] = f"Q0_PPPOE,{queueSizeBytes};"

            shaperSpeedHighKBit = round((account.down_speed_mbit * 1000) * 0.9)
            shaperSpeedLowKBit = round((account.down_speed_mbit * 1000) * 0.98)

            radiusAttribute["RtBrick-QoS-Shaper"] = \
                f"name=ACCESS_SHAPER,high={shaperSpeedHighKBit},low={shaperSpeedLowKBit};"

        if account.up_speed_mbit:
            # Set CBS to 10th of bandwidth (to allow about 100 ms of burst)

            cbsKBit = round((account.up_speed_mbit * 1000) / 100)
            cirKBit = round((account.up_speed_mbit * 1000) * 0.98)

            levelStrings = [
                f"level=1,cir={cirKBit},cbs={cbsKBit};"
                f"level=2,cbs={cbsKBit};"
                f"level=3,cbs={cbsKBit};"
                f"level=4,cbs={cbsKBit};"
            ]

            radiusAttribute["RtBrick-QoS-Policer"] = "".join(levelStrings)

        return JsonResponse(status=200, data=radiusAttribute)
