#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from twisted.python import log
from twisted.web import resource, server
from Load.loadconfig import load
from Devices.WebService.SOAPQuoter import *
from Devices.WebService.XMLRPCQuoter import *  
from Devices.WebService.RESETQuoter import * 
import sys


def main():
    from twisted.internet import reactor
    log.startLogging(sys.stdout);
    root = resource.Resource()
    root.putChild('RPC2', XMLRPCQuoter())
    root.putChild('SOAP', SOAPQuoter())
    root.putChild('RESET',RESETQuoter())
    reactor.listenTCP(int(load('WebService', 'Port')), server.Site(root))
    reactor.run()

if __name__ == '__main__':
    main()