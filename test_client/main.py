import sys
from pyrad.client import Client
from pyrad.dictionary import Dictionary
import pyrad.packet


def radius_auth(username, password, is_pppoe = False):
    srv = Client(server="127.0.0.1", authport=1812, secret=b"testing123",
                 dict=Dictionary("test_client/dictionaries/dictionary"))

    # create request
    req = srv.CreateAuthPacket(
        code=pyrad.packet.AccessRequest,
        User_Name=username,
        # IP of BNG
        NAS_IP_Address="10.43.0.1",
        NAS_Identifier="lrma0001",
        NAS_Port_Id="lrma0001#ifp-0/0/4#300#0##",
        NAS_Port="68337664",
        NAS_Port_Type="15",
        Service_Type="2",
        Acct_Session_Id="216454257090504779:1752499609",
        RtBrick_Access_Hostname="lrma0001",
        RtBrick_Access_Port="ifp-0/0/4",
        RtBrick_Access_Stack="v:300",
        RtBrick_Access_MAC_Address="00:25:90:bd:3a:59",
        RtBrick_Subscriber_Id=3,
        RtBrick_Subscriber_Ifl="ipoe-0/0/4/216454257090504779",
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
