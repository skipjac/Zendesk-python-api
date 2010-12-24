# -*- coding: utf-8 -*-

from xml.dom import pulldom
import re
import sys 
import os 
import httplib2
import base64

h= httplib2.Http(".cache")
base64string = base64.encodestring('%s:%s' % ('adminlogin', 'password'))
#download the XML back up from your zendesk and place it in a directory 
#this is the link to the file
doc = pulldom.parse("dir/organizations.xml")
for event, node in doc:
    if event == pulldom.START_ELEMENT and node.localName == "organization":
        doc.expandNode(node) 
        #get the organization ID
        orgIDold = node.getElementsByTagName("id")
        #get the name 
        orgName = node.getElementsByTagName("name")
        #get the creation time
        orgCreated = node.getElementsByTagName("created-at")
        #search for the creation time you want to delete. 
        if re.search("2010-12-21", orgCreated[0].firstChild.data):
            #console print of the organizations 
            print orgIDold[0].firstChild.data + " "+ orgName[0].firstChild.data+" "+orgCreated[0].firstChild.data
            #the call to DELETE the org's
            resp, content = h.request("https://your zendesk url/organizations/"+orgIDold[0].firstChild.data+".xml", "DELETE",
            headers={'content-type' : 'application/xml ', 'Authorization': 'Basic %s' % base64string,} )
            #print the response from zendesk. 
            print resp
