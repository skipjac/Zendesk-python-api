
import sys 
import os 
import httplib2
import base64

h= httplib2.Http(".cache")
#encode the basic authentication in base 64
base64string = base64.encodestring('%s:%s' % ("skip@example.net", "Password"))
#create the xml with html encoding and escaping 
resp, content = h.request("http://helpdesk.zendesk.com/entries.xml", "POST",  body="<entry><forum-id>66730</forum-id>\
<submitter-id>5766145</submitter-id>\
<title>Test with html 3</title>\
<body>&lt;p&gt;the quick brown fox jumps over the lazy dog&lt;/p&gt;\
&lt;script type=\"text/javascript\"&gt;// &lt;![CDATA[\
\
$j('div.user_formatted').append(\"&lt;iframe src =\\\"http://www.skipjack.info\\\" width=\\\"100%\\\" height=\\\"300\\\"&gt;&lt;p&gt;test&lt;/p&gt;&lt;/iframe&gt;\");\
// ]]&gt;&lt;/script&gt;</body>\
<current-tags>test1 test2</current-tags>\
<is-locked>false</is-locked><is-pinned>false</is-pinned>\
</entry>",
headers={'content-type' : 'application/xml' , 'Authorization': 'Basic %s' % base64string,} )
print content
print resp
#if a 201 is returned then the new entry url is in the location of the header. 
print resp['location']
