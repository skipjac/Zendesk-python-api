# -*- coding: utf-8 -*-

from xml.dom import pulldom
from urlparse import urlparse
import re
import sys 
import os 
import httplib2


#creates a new goup on the target system 
def createGroupZendesk (gName):
    h= httplib2.Http(".cache")
    h.add_credentials('user@email.com', 'Password')
    resp, content = h.request("http://sandbox1284059247.zendesk.com/groups.xml", "POST",  body="<group>\
    <name>"+gName+"</name>\
    </group>",
    headers={'content-type' : 'application/xml'} )
    print content
    print resp
    if resp['status'] == '201':
        locationID = urlparse(resp['location'])
        #print locationID.path
        (dirName,  newID) = os.path.split(locationID.path)
        (gnewID,  pathExt) = os.path.splitext(newID)
        #print gnewID
    return gnewID



#this is where the look up for the old and new group ID are. 
f2 = open('oldgroups.xml',  'w')
doc = pulldom.parse("skipjack-xml/groups.xml")
f2.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<groups-conv>\n")

#opens the groups.xml and walks thorugh it 
for event, node in doc:
    if event == pulldom.START_ELEMENT and node.localName == "group":
        doc.expandNode(node) 
        groupIDold = node.getElementsByTagName("id")
        groupName = node.getElementsByTagName("name")
        groupCreated = node.getElementsByTagName("created-at")
        #prints the XML data
        print groupIDold[0].firstChild.data + ","+ groupName[0].firstChild.data+","+groupCreated[0].firstChild.data
        newGroupName = str(groupName[0].firstChild.data)
        newGroupID = createGroupZendesk(newGroupName)
        print "<old-group>"+ str(groupName[0].firstChild.data)+"</old-group>\n"
        f2.write("<group>\n<old-group>"+ str(groupIDold[0].firstChild.data)+"</old-group>\n<new-group>"+newGroupID+"</new-group>\n</group>\n")
        
        print newGroupID

f2.write("</groups-conv>")
f2.close()
