import sys 
import os 
import httplib2
import simplejson

h= httplib2.Http(".cache")
h.add_credentials('skip@meail.com', 'Password')
resp, content = h.request("http://yourzendesk.zendesk.com/tickets.json", "POST",  body="ticket:\
{\
\"subject\":\"Some thing over the rainbow\",\
\"description\":\"with date field set to 5\",\
\"requester_id\":\"13323731\"}",
    headers={'content-type' : 'application/json'} )
print resp
print content
print resp['location']
