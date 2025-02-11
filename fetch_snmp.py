host = '192.168.10.15'
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *


@asyncio.coroutine
def run():
    snmpEngine = SnmpEngine()

    iterator = getCmd(
        snmpEngine,
        CommunityData('public', mpModel=0),
        UdpTransportTarget(('demo.snmplabs.com', 161)),
        ContextData(),
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
    )

    errorIndication, errorStatus, errorIndex, varBinds = yield from iterator

    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
        )
              )
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))

    snmpEngine.transportDispatcher.closeDispatcher()


asyncio.get_event_loop().run_until_complete(run())