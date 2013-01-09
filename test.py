import logging, hmac, hashlib, base64
from datetime import datetime
from suds.client import Client
from suds.sax.element import Element
import sys

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
#logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

client = Client('file:///home/esuser/workspace/test/WebContent/designlink.wsdl', location='https://uk.farnell.com/pffind/services/SearchService', faults=False, headers={'Content-Type': 'text/html'}, xstq=True, prefixes=True)
print client

def do_auth(client, operation):
	accountname = "CadSoft2"
	password = "CadSoft2"

	timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000")
	sha1 = hashlib.sha1()
	hmac_obj = hmac.new(password, operation + timestamp, hashlib.sha1)
	digest = hmac_obj.digest()
	signature = base64.b64encode(digest)

	ssnns = ('v1', 'http://pf.com/soa/services/v1')
	userinfo = Element('userInfo', ns=ssnns)
	userinfo.append(Element('signature', ns=ssnns).setText(signature))
	userinfo.append(Element('timestamp', ns=ssnns).setText(timestamp))
	userinfo.append(Element('locale', ns=ssnns).setText('en_UK'))
	acctinfo = Element('accountInfo', ns=ssnns)
	acctinfo.append(Element('customerId', ns=ssnns).setText(accountname))
	client.set_options(soapheaders=(userinfo,acctinfo))

do_auth(client, 'searchByKeyword')
print client.service.searchByKeyword('LM324', 0, 50)

do_auth(client, 'searchByPremierFarnellPartNumber')
print client.service.searchByPremierFarnellPartNumber('1861629')

