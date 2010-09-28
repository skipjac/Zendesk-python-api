#this is for a agent create
import sys 
import os 
import httplib2
import simplejson

h= httplib2.Http(".cache")
h.add_credentials('login@something.net', 'Password')
resp, content = h.request("http://yourhelpdesk.zendesk.com/tickets.xml", "POST",  body="<ticket><subject>Some thing over the rainbow</subject>\
<description>with date field set to 5</description>\
<assignee-id>5766145</assignee-id>\
<set-tags>happy</set-tags>\
<requester-email>mail@evidensys.com</requester-email>\
<priority-id>3</priority-id>\
<status-id>3</status-id>\
<ticket-type-id>4</ticket-type-id>\
<ticket-field-entries type=\"array\">\
<ticket-field-entry>\
<ticket-field-id>139051</ticket-field-id>\
<value>5</value>\
</ticket-field-entry>\
</ticket-field-entries>\
</ticket>",
    headers={'content-type' : 'application/xml'} )
print resp
print content
print resp['location']
