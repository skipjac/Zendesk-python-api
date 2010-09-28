 # -*- coding: utf-8 -*-
import sys 
import os 
import httplib2
import simplejson

h= httplib2.Http(".cache")
h.add_credentials('email@email,com', 'Password')
resp, content = h.request("http://zendeskname.zendesk.com/tickets/557.xml", "PUT",  body="<ticket>\
<current-collaborators>Bob Nine</current-collaborators>\
</ticket>",
    headers={'content-type' : 'application/xml'} )
print content
print resp
#print resp['location']
