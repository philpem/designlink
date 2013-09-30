import logging, hmac, hashlib, base64
from datetime import datetime
from suds.client import Client
from suds.sax.element import Element
import sys

from urllib import pathname2url
import os
#wsdl_url = 'file:' + pathname2url(os.path.join(os.path.dirname(os.path.realpath(__file__)), "designlink.wsdl"))
wsdl_url = 'https://uk.farnell.com/pffind/services/SearchService?wsdl'

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
#logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

client = Client(wsdl_url, location='https://uk.farnell.com/pffind/services/SearchService', faults=False, headers={'Content-Type': 'text/html'}, xstq=True, prefixes=True)
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

print "-------- Search By Keyword LM324"
do_auth(client, 'searchByKeyword')
print client.service.searchByKeyword('LM324', 0, 50)

print "-------- Search By Premier Farnell Part Number (intended failure)"
do_auth(client, 'searchByPremierFarnellPartNumber')
print client.service.searchByPremierFarnellPartNumber('1861629')

print "-------- Search By Premier Farnell Part Number (intended success)"
do_auth(client, 'searchByPremierFarnellPartNumber')
print client.service.searchByPremierFarnellPartNumber('2084573')

