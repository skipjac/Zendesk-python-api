#agent create on behalf of end user
# -*- coding: utf-8 -*-
import sys 
import os 
import httplib2
import simplejson

h= httplib2.Http(".cache")
h.add_credentials('agent@example.net', 'Password')
resp, content = h.request("http://yourhelpdesk.zendesk.com/tickets.xml", "POST",  body="<ticket><subject>the user should be skip @ zendesk take 3</subject>\
<description>Die im Betreff angegebene Problematik ist bereits in der Vergangenheit aufgetreten. Damals wurde offenbar die Anzahl der Datenbankthreads erhöht. Wirklich geholfen hat es nicht, es treten zwei Fehlerbilder auf, siehe Screenshots.Da nun der Klient 329 mit voraussichtlich deutlich höheren Volumen als327 und 328 produktiv geht, besteht hier Handlungsbedarf.</description>\
<priority-id>3</priority-id>\
<status-id>0</status-id>\
<ticket-type-id>3</ticket-type-id>\
<ticket-field-entries type=\"array\">\
<ticket-field-entry>\
<ticket-field-id>104609</ticket-field-id>\
<value>sad</value>\
</ticket-field-entry>\
</ticket-field-entries>\
</ticket>",
    headers={'content-type' : 'application/xml' ,'On-Behalf-of' : 'skip@example.com'} )
print content
print resp
print resp['location']
