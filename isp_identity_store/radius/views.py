from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views import View

from accounts.models import Account


class AuthView(View):

    def find_account(self, **args) -> Account | None:
        pass

    def get(self, request, **args):

        account = self.find_account(**args)

        if not account:
            return JsonResponse(status=401, data={"Reply-Message": "Home-ID is not valid"})

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


class AuthHomeIdView(AuthView):

    def find_account(self, home_id):
        return Account.objects.filter(home_id=home_id).first()
