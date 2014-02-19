import logging
from designlink import DesignLinkClient

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.ERROR)
logging.getLogger('suds.transport').setLevel(logging.ERROR)
logging.getLogger('suds.xsd.schema').setLevel(logging.ERROR)
logging.getLogger('suds.wsdl').setLevel(logging.ERROR)

wr = DesignLinkClient()

print "--- Search By Keyword ---"
print wr.searchByKeyword('LM324', 0, 50)

print "--- Search By Part Number (with nonexistent part number) ---"
print wr.searchByPremierFarnellPartNumber('1861629')

print "--- Search By Part Number (with valid part number) ---"
print wr.searchByPremierFarnellPartNumber('2084573')
