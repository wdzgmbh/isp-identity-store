import codecs
from django.contrib.auth.hashers import check_password

from django.http import JsonResponse
from django.utils import timezone
from ipaddress import IPv4Network, IPv6Network
from rest_framework import authentication, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin, ModelViewSet, ViewSet

from accounts.models import Account, Session


class RadiusViewSet(ViewSet):
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

    def _get_account_from_request(self, request, validate=True):
        Framed_Protocol = self._get_value_from_request(request, "Framed-Protocol")
        account = None
        if Framed_Protocol:
            User_Name = self._get_value_from_request(request, "User-Name")
            User_Password = self._get_value_from_request(request, "User-Password")
            account = Account.objects.filter(user=User_Name).first()

            if not account:
                return None, JsonResponse(status=401, data={"Reply-Message": "User is not valid"})

            if validate and not check_password(User_Password, account.password):
                return None, JsonResponse(status=401, data={"Reply-Message": "Password is not valid"})

        else:
            ADSL_Agent_Circuit_Id = self._get_value_from_request(request, 'ADSL-Agent-Circuit-Id')
            account = Account.objects.filter(line_id=ADSL_Agent_Circuit_Id).first()
            if not account:
                return None, JsonResponse(status=401, data={"Reply-Message": "LineID is not valid"})

        return account, None


class RadiusAccountingView(RadiusViewSet):

    def post(self, request, format=None):

        account, resp  = self._get_account_from_request(request, validate=False)
        if resp:
            return resp

        Acct_Status_Type = self._get_value_from_request(request, "Acct-Status-Type")
        Acct_Session_Id = self._get_value_from_request(request, "Acct-Session-Id")
        ADSL_Agent_Circuit_Id = self._get_value_from_request(request, 'ADSL-Agent-Circuit-Id')
        ADSL_Agent_Remote_Id = self._get_value_from_request(request, 'ADSL-Agent-Remote-Id')
        Framed_IP_Address = self._get_value_from_request(request, 'Framed-IP-Address')
        Framed_IP_Netmask = self._get_value_from_request(request, 'Framed-IP-Netmask')
        Framed_IPv6_Prefix = self._get_value_from_request(request, 'Framed-IPv6-Prefix')
        Delegated_IPv6_Prefix = self._get_value_from_request(request, 'Delegated-IPv6-Prefix')

        existing_session = account.session_set.filter(
            session_id=Acct_Session_Id
        ).first()

        if Acct_Status_Type in ['Start', "Interim-Update"]:

            if existing_session:
                print(f"Updating {existing_session}")
                existing_session.last_seen_at = timezone.now()
                existing_session.save()
            else:
                print(f"Creating Session for acount {account}")
                Session.objects.create(
                    account=account,
                    session_id=Acct_Session_Id,
                    remote_id=ADSL_Agent_Remote_Id,
                    circuit_id=ADSL_Agent_Circuit_Id,

                    ip_address=IPv4Network(f"{Framed_IP_Address}/{Framed_IP_Netmask}").with_prefixlen,
                    ipv6_prefix=IPv6Network(Framed_IPv6_Prefix).with_prefixlen,
                    ipv6_pd_prefix=IPv6Network(Delegated_IPv6_Prefix).with_prefixlen,
                )

        if Acct_Status_Type in ['Stop']:
            print(f"Terminating {existing_session}")
            existing_session.last_seen_at = timezone.now()
            existing_session.terminated_at = timezone.now()
            existing_session.save()

        return JsonResponse(status=200, data={})

class RadiusAuthenticateView(RadiusViewSet):

    def post(self, request, format=None):

        account, failure_response = self._get_account_from_request(request)
        if failure_response:
            return failure_response

        return JsonResponse(status=200, data={})


class RadiusAuthorizeView(RadiusViewSet):

    def post(self, request, format=None):

        account, failure_response = self._get_account_from_request(request)
        if failure_response:
            return failure_response

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
        replyMessage = ""

        if account.down_speed_mbit:
            replyMessage += f"SRD={round(account.down_speed_mbit * 1000)}#"

            # Set the queue size to 4 ms of the shaped bandwidth
            queueSizeBytes = round((account.down_speed_mbit * 1000) * 1024 / 8 * 0.004)
            radiusAttribute["RtBrick-QoS-Queues"] = f"Q0_PPPOE,{queueSizeBytes};"

            shaperSpeedHighKBit = round((account.down_speed_mbit * 1000) * 0.9)
            shaperSpeedLowKBit = round((account.down_speed_mbit * 1000) * 0.98)

            radiusAttribute["RtBrick-QoS-Shaper"] = \
                f"name=ACCESS_SHAPER,high={shaperSpeedHighKBit},low={shaperSpeedLowKBit};"

        if account.up_speed_mbit:
            replyMessage += f"SRU={round(account.up_speed_mbit * 1000)}#"

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

        replyMessage += f"LID={account.line_id}#"
        radiusAttribute["Reply-Message"] = replyMessage

        return JsonResponse(status=200, data=radiusAttribute)
