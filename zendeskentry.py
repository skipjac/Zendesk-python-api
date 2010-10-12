
import sys 
import os 
import httplib2
import simplejson
import base64

h= httplib2.Http(".cache")
base64string = base64.encodestring('%s:%s' % ("skip@email.net", "Password"))
resp, content = h.request("http://yourdomain.zendesk.com/entries.xml", "POST",  body="<entry>\
<forum-id>66731</forum-id>\
<title>Feedback: reminder</title>\
<body>aaaaaaa</body>\
<current-tags></current-tags>\
<is-locked>false</is-locked>\
<is-pinned>false</is-pinned>\
</entry>",
headers={'content-type' : 'application/xml' , 'Authorization': 'Basic %s' % base64string,  } )
print content
print resp
print resp['location']
