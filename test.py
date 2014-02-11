import logging, hmac, hashlib, base64
from datetime import datetime
from suds.client import Client as SudsClient


class FDLClient(object):
    """ DesignLink client object """    
    
    suds_types = []
    """List of the SOAP Api types"""
    suds_methods = []
    """List of the SOAP Api methods"""
    soap_endpoint = None
    """SOAP endpoint"""
    user_id = None
    """SOAP user ID"""
    encryption_key = None
    """SOAP encryption key"""
    suds_client = None
    """Consolidated API for consuming web services"""

    def __init__(self, soap_endpoint = 'https://uk.farnell.com/pffind/services/SearchService', user_id = "CadSoft2", encryption_key = "CadSoft2"):
        """
        Instantiate the suds client and add the SOAP types and methods to the list of attributes
        """
        self.soap_endpoint = soap_endpoint
        self.user_id = user_id
        self.encryption_key = encryption_key

        self.suds_client = SudsClient('https://uk.farnell.com/pffind/services/SearchService?wsdl',
                                      location=soap_endpoint,
                                      faults=False,
                                      headers={'Content-Type': 'text/html'},
                                      xstq=True,
                                      prefixes=True
                                     )
        # Make easy the access to the types and methods
        for suds_type in self.suds_client.sd[0].types:
            self.suds_types.append(suds_type[0].name)
        for suds_method in self.suds_client.sd[0].service.ports[0].binding.operations:
            self.suds_methods.append(suds_method)

    def __getattribute__(self, name):
        """
        Lookup SOAP types and methods first.
        If the attribute is not a SOAP type or method, try to return an attribute of the class.
        """
        if name not in ('suds_types', 'suds_methods') and name in self.suds_types:
            # if the attribute is one of the SOAP types
            return self.suds_client.factory.create(name)
        elif name not in ('suds_types', 'suds_methods') and name in self.suds_methods:
            # if the attribute is one of the SOAP methods
            self.set_header(name)
            return self.suds_client.service.__getattr__(name)
        else:
            return super(FDLClient, self).__getattribute__(name)

    def set_header(self, operation):
        """
        Fill in the SOAP headers with the DesignLink command data
        """
        userinfo = self.UserInfo
        acctinfo = self.AccountInfo

        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000")
        hmac_obj = hmac.new(self.encryption_key, operation + timestamp, hashlib.sha1)
        digest = hmac_obj.digest()
        signature = base64.b64encode(digest)

        userinfo.signature = signature
        userinfo.timestamp = timestamp
        userinfo.locale = 'en_UK'
        acctinfo.customerId = self.user_id
        self.suds_client.set_options(soapheaders=(userinfo,acctinfo))

 
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.ERROR)
logging.getLogger('suds.transport').setLevel(logging.ERROR)
logging.getLogger('suds.xsd.schema').setLevel(logging.ERROR)
logging.getLogger('suds.wsdl').setLevel(logging.ERROR)

wr = FDLClient()

print "--- Search By Keyword ---"
print wr.searchByKeyword('LM324', 0, 50)

print "--- Search By Part Number (with nonexistent part number) ---"
print wr.searchByPremierFarnellPartNumber('1861629')

print "--- Search By Part Number (with valid part number) ---"
print wr.searchByPremierFarnellPartNumber('2084573')
