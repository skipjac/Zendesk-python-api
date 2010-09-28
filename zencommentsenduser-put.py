 #end user add comment
 # -*- coding: utf-8 -*-
import sys 
import os 
import httplib2
import simplejson

h= httplib2.Http(".cache")
h.add_credentials('suser@exmaple.com', 'Password')
resp, content = h.request("http://yourhelpdesk.zendesk.com/requests/194.xml", "PUT",  body="<comment>\
<is-public>true</is-public>\
<value>This is a comment 8</value>\
</comment>",
    headers={'content-type' : 'application/xml'  } )
print content
print resp
#print resp['location']
