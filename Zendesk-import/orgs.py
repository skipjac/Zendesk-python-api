# -*- coding: utf-8 -*-

from xml.dom import pulldom
from urlparse import urlparse
import urllib
import re
import sys 
import os 
import httplib2
import StringIO


#the old organizations
doc = pulldom.parse("skipjack-xml/organizations.xml")

#this is the url to find a exsisting org in the target zendesk if a 406 is generated on org creation
SEARCHUSER = "http://sandbox1284059247.zendesk.com/people.xml?query=organization:%s"

#pulls in the old Group id with the new target systems groupID
def groupIDcompare(oldid):
    oldgroupdoc = pulldom.parse("oldgroups.xml")
    for event, node in oldgroupdoc:
     if event == pulldom.START_ELEMENT and node.localName == "group":
         oldgroupdoc.expandNode(node) 
         groupIDold = node.getElementsByTagName("old-group")
         groupIDnew = node.getElementsByTagName("new-group")
         groupIDoldData = str(groupIDold[0].firstChild.data)
         groupidnewData = str(groupIDnew[0].firstChild.data)
         if groupIDoldData == oldid:
             return groupidnewData
         print groupIDold[0].firstChild.data + ","+ groupIDnew[0].firstChild.data
         

#if the Organization exists in the new system we group the target systems ID and return it 
def getExistingorgID (foundorg):
    url = SEARCHUSER % urllib.quote_plus("\""+foundorg+"\"")
    print url
    h= httplib2.Http(".cache")
    h.add_credentials('user@email.com', 'Password')
    resp,  content = h.request(url, "GET", headers={'content-type' : 'application/xml'} )
    formattedResp = StringIO.StringIO(content)
    parsedRecord = pulldom.parse(formattedResp)
    #print parsedRecord.toxml()
    for event, node in parsedRecord:
     if event == pulldom.START_ELEMENT and node.localName == "record":
        parsedRecord.expandNode(node)
        groupIDold = node.getElementsByTagName("id")
        ExistingUserID = str(groupIDold [0].firstChild.data)
        print ExistingUserID +" inside function"
        return ExistingUserID

#uses the API to create the new organization in the target system. 
def createOrganizationZendesk (oName, oGroup, oShared, oNotes, oDetails, oSharedComment, oDefault):
    h= httplib2.Http(".cache")
    h.add_credentials('user@email.com', 'Password')
    resp, content = h.request("http://sandbox1284059247.zendesk.com/organizations.xml", "POST",  body="<organization>\
    <name>"+oName+"</name>\
    <notes>"+oNotes+"</notes>\
    <details>"+oDetails+"</details>\
    <is-shared type=\"boolean\">"+oShared+"</is-shared>\
    <is-shared-comments type=\"boolean\">"+oSharedComment+"</is-shared-comments>\
    <group-id>"+oGroup+"</group-id>\
    <default>"+oDefault+"</default>\
    </organization>",
    headers={'content-type' : 'application/xml'} )
    print content
    print resp
    if resp['status'] == '201':
        locationID = urlparse(resp['location'])
        #print locationID.path
        (dirName,  newID) = os.path.split(locationID.path)
        (onewID,  pathExt) = os.path.splitext(newID)
        print onewID
        return onewID
    elif resp['status'] == '406':
        onewID = getExistingorgID(oName)
        print onewID
        return onewID
    print onewID


#this is were the look XML is written 
f2 = open('oldorgs.xml',  'w')
f2.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<orgs-conv>\n")

#this is were the old organizations.xml is opened and walked through 
for event, node in doc:
    if event == pulldom.START_ELEMENT and node.localName == "organization":
        doc.expandNode(node) 
        orgIDold = node.getElementsByTagName("id")
        orgid = str(orgIDold[0].firstChild.data)
        orgNameold = node.getElementsByTagName("name")
        Orgname = str(orgNameold[0].firstChild.data)
        orgNotesold = node.getElementsByTagName("notes")
        if orgNotesold[0].firstChild != None:
            Orgnotes = str(orgNotesold[0].firstChild.data)
        else: 
            Orgnotes = ""
        orgDetailsold = node.getElementsByTagName("details")
        if orgDetailsold[0].firstChild != None:
            Orgdetails = str(orgDetailsold[0].firstChild.data)
        else:
            Orgdetails = ""
        
        orgSharedold = node.getElementsByTagName("is-shared")
        Orgshared = str(orgSharedold[0].firstChild.data)
        orgScommentsold = node.getElementsByTagName("is-shared-comments")
        Orgscomment = str(orgScommentsold[0].firstChild.data)
        orgGroupIDold = node.getElementsByTagName("group-id")
        if orgGroupIDold[0].firstChild != None:
            Groupid = str(orgGroupIDold[0].firstChild.data)
            newID = groupIDcompare(Groupid)
        else: 
            newID = ""
        
        
        orgDefaultold = node.getElementsByTagName("default")
        if orgDefaultold[0].firstChild != None:
            Orgdefault= str(orgDefaultold[0].firstChild.data)
        else: 
            Orgdefault = ""
       
        
        newOrgID = createOrganizationZendesk(Orgname, newID, Orgshared, Orgnotes, Orgdetails, Orgscomment, Orgdefault)
        #writes the old org ID with the new org ID 
        f2.write("<org>\n<old-org>"+ orgid+"</old-org>\n<new-org>"+newOrgID+"</new-org>\n</org>\n")
        print orgIDold[0].firstChild.data + " "+ orgNameold[0].firstChild.data+" new group "+newID+" neworg "+newOrgID
f2.write("</orgs-conv>")
f2.close()
