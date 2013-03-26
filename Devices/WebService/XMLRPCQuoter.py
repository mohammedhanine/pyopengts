from twisted.web import xmlrpc
from Event.WebService.UserEvent import user

class XMLRPCQuoter(xmlrpc.XMLRPC):
    def xmlrpc_headerValue(self, request, headerName):
        return request.requestHeaders.getRawHeaders(headerName)
    def xmlrpc_add(self,a=0,b=0):
        u=user()
        return u.useradd(a, b)
