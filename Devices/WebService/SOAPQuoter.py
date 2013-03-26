from twisted.web import soap
from Event.WebService.UserEvent import user


class SOAPQuoter(soap.SOAPPublisher):
    def soap_add(self,a=0,b=0):
        u=user()
        return u.useradd(a, b)
    def soap_headerValue(self, request, headerName):
        return request.requestHeaders.getRawHeaders(headerName)
    def soap_buscartx(self,imei):
        u=user()
        return u.buscaruser(imei=imei)
    
class SOAPQuoterUser(soap.SOAPPublisher):
    def soap_auth(self,imie="",login=""):
        return login