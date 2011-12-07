# -*- coding: utf-8 -*-

from xml.etree.ElementTree import ElementTree
import codecs
import re
import os.path
import httplib2
import simplejson
import base64

def deleteTicket(data):
    print data
    h= httplib2.Http(".cache")
    auth_string = 'skip@techassistant.net/token:123--token--goes--here'
    auth_byte = auth_string.encode('utf-8')
    base64string = base64.b64encode(auth_byte)
    resp, content = h.request("http://skipjack.zendesk.com/tickets/"+str(data), "DELETE",  
    headers={'content-type' : 'application/json', 'Authorization': 'Basic %s' % base64string  } )
    print resp, content 

#this is the call with the ticket number
deleteTicket(1054)
