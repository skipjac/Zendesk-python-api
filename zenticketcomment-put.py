#adding comments as agent 
# -*- coding: utf-8 -*-
import sys 
import os 
import httplib2

h= httplib2.Http(".cache")
h.add_credentials('agent@example.net', 'Password')
resp, content = h.request("http://skipjack.zendesk.com/tickets/620.xml", "PUT",  body="<ticket><comment>\
<is-public>true</is-public>\
<external-id>TEST-1</external-id>\
<value>adding external id</value>\
</comment>\
</ticket>",
    headers={'content-type' : 'application/xml'} )
print content
print resp
#print resp['location']
