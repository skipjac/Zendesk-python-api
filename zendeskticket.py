#end user ticket create
import sys 
import os 
import httplib2


h= httplib2.Http(".cache")
h.add_credentials('user@example.com', 'Password')
resp, content = h.request("http://yourhelpdesk.zendesk.com/requests.xml", "POST",  body="<ticket><subject>make me some tags with fields</subject>\
<description>without the created \r \r  ryryryryr yryryry </description>\
<set-tags>skipppie</set-tags>\
<ticket-field-entries type=\"array\">\
<ticket-field-entry>\
<ticket-field-id type=\"integer\">104609</ticket-field-id>\
<value>beepling_computer</value>\
</ticket-field-entry>\
</ticket-field-entries>\
</ticket>",
    headers={'content-type' : 'application/xml'} )
print content
print resp
print resp['location']
