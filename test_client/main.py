import sys
import time

from pyrad.client import Client
from pyrad.dictionary import Dictionary
import pyrad.packet
from random import randrange


# AttrAcctStatusType AcctInterimUpdate
# AttrUserName "a-412003-74851-0001"
# AttrNASIPAddress "10.44.3.15"
# AttrNASIdentifier "trmc2002"
# AttrNASPortId "trmc2002#ifp-0/1/26#855#0#KDKD0086 0/08:0855#00:e0:df:da:84:55"
# AttrNASPort 1513451520
# AttrNASPortType NptEthernet
# AttrServiceType StFramed
# AttrFramedProtocol FpPPP
# AttrFramedIPAddress "100.71.226.124"
# AttrFramedIPNetmask "255.255.255.255"
# AttrFramedIPv6Prefix "2a01:585:c00f:806e::/64"
# AttrDelegatedIPv6Prefix "2a01:585:c401:2900::/56"
# AttrAcctSessionId "72339069015850919:1776695187"
# AttrAcctAuthentic AuthenticRADIUS
# AttrEventTimestamp 1778063189
# AttrAcctInputOctets 3534155886
# AttrAcctOutputOctets 675181027
# AttrAcctInputPackets 169681528
# AttrAcctInputGigawords 4
# AttrOutputPackets 414843183
# AttrAcctOutputGigawords 129
# AttrAcctSessionTime 1368001
# DSLForumAgentCircuitId "KDKD0086 0/08:0855"
# DSLForumAgentRemoteId "00:e0:df:da:84:55"
# DSLForumActualDataRateUpstream 40659
# DSLForumActualDataRateDownstream 102209
# DSLForumAttainableDataRateUpstream 55621
# DSLForumAttainableDataRateDownstream 0
# RtBrick-Class-0-Packets-Out 414843183
# RtBrick-Class-0-Bytes-Out 554725962211
# RtBrick-Class-1-Packets-Out 0
# RtBrick-Class-1-Bytes-Out 0
# RtBrick-Class-2-Packets-Out 0
# RtBrick-Class-2-Bytes-Out 0
# RtBrick-Class-3-Packets-Out 0
# RtBrick-Class-3-Bytes-Out 0
# RtBrick-Class-4-Packets-Out 0
# RtBrick-Class-4-Bytes-Out 0
# RtBrick-Class-5-Packets-Out 0
# RtBrick-Class-5-Bytes-Out 0
# RtBrick-Class-6-Packets-Out 0
# RtBrick-Class-6-Bytes-Out 0
# RtBrick-Class-7-Packets-Out 0
# RtBrick-Class-7-Bytes-Out 0
# RtBrick-PolicerL1PacketsIn 169681528
# RtBrick-PolicerL1BytesIn 20714025070
# RtBrick-PolicerL2PacketsIn 0
# RtBrick-PolicerL2BytesIn 0
# RtBrick-PolicerL3PacketsIn 0
# RtBrick-PolicerL3BytesIn 0
# RtBrick-PolicerL4PacketsIn 0
# RtBrick-PolicerL4BytesIn 0
# RtBrick-AccessHostname "trmc2002"
# RtBrick-AccessPort "ifp-0/1/26"
# RtBrick-AccessStack "v:855"
# RtBrick-AccessMACAddress "f0:a7:31:e7:6f:6b"
# RtBrick-SubscriberId 72339069015850919
# RtBrick-SubscriberIfil "ppp-0/1/26/72339069015850919"


def radius_auth(username, password, is_pppoe = False):
    srv = Client(server="127.0.0.1", authport=1812, secret=b"testing123",
                 dict=Dictionary("test_client/dictionaries/dictionary"))

    session_id = randrange(2142000000000000,2143000000000000)
    subscriber_id = randrange(1752400000,1752499999)

    # create request
    req = srv.CreateAuthPacket(
        code=pyrad.packet.AccessRequest,
        User_Name=username,
        Acct_Session_Id=f"{session_id}:{subscriber_id}",
        ADSL_Agent_Circuit_Id="DEU.WDZG01.WOB2738425",
        ADSL_Agent_Remote_Id="ec0032.ce.as9136.net",
    )

    if is_pppoe:
        req["Framed-Protocol"] = "PPP"

    req["User-Password"] = req.PwCrypt(password)

    # send request
    reply = srv.SendPacket(req)

    if reply.code == pyrad.packet.AccessAccept:
        print("access accepted")
    else:
        print("access denied")

    print("Attributes returned by server:")
    for i in reply.keys():
        print("%s: %s" % (i, reply[i]))


    accounting_pkt = srv.CreateAcctPacket(
        code=pyrad.packet.AccountingRequest,
        Acct_Status_Type="Start",
        User_Name=username,
        Acct_Session_Id=f"{session_id}:{subscriber_id}",
        Framed_IP_Address= "100.71.226.124",
        Framed_IP_Netmask="255.255.255.255",
        Framed_IPv6_Prefix="2a01:585:c00f:806e::/64",
        Delegated_IPv6_Prefix="2a01:585:c401:2900::/56",
        ADSL_Agent_Circuit_Id="DEU.WDZG01.WOB2738425",
        ADSL_Agent_Remote_Id="ec0032.ce.as9136.net",
    )

    srv.SendPacket(accounting_pkt)

    time.sleep(5)

    accounting_pkt['Acct-Status-Type'] = "Interim-Update"
    srv.SendPacket(accounting_pkt)

    time.sleep(5)

    accounting_pkt["Acct-Status-Type"] = "Stop"
    srv.SendPacket(accounting_pkt)


def main_pppoe():
    radius_auth("testeroni", "testeroni123", is_pppoe=True)


def main_ipoe():
    radius_auth("00:25:90:bd:3a:59@ipoe", "ipoe")



def main() -> int:
    main_ipoe()
    main_pppoe()
    return 0


if __name__ == '__main__':
    sys.exit(main())
