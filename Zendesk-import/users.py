
# -*- coding: utf-8 -*-
from xml.dom import pulldom
from urlparse import urlparse
import urllib
import re
import sys 
import os 
import httplib2
import StringIO

doc = pulldom.parse("skipjack-xml/users.xml")

#this is the url to find a exsisting user in the target zendesk if a 406 is generated on user creation
SEARCHUSER = "http://sandbox1284059247.zendesk.com/people.xml?query=%s"
#this is the file to write new ID's in a XML format linking them to the old ID
f2 = open('oldusers.xml',  'w')

#finds the old org ID and returns the new org ID so the user can be created.
def orgIDcompare(oldid):
   
    print oldid+" old org id"
    oldorgdoc = pulldom.parse("oldorgs.xml")

    for event, node in oldorgdoc:
  
     if event == pulldom.START_ELEMENT and node.localName == "org":
         oldorgdoc.expandNode(node) 
         orgIDold = node.getElementsByTagName("old-org")
         orgIDnew = node.getElementsByTagName("new-org")
         orgIDoldData = str(orgIDold[0].firstChild.data)
         orgidnewData = str(orgIDnew[0].firstChild.data)
         if orgIDoldData == oldid:
             return orgidnewData
             print orgidnewData +" new ord id found"


#If the email aready exists in the target system this will look it up and return the new ID so it can be written to the oldusers.xml file
def getExistingUserID (foundemail):
    url = SEARCHUSER % urllib.quote_plus(foundemail)
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
        print ExistingUserID +" inside found user got id function"
        return ExistingUserID

#this creates the new user and returns the new ID 
def createUserZendesk (uName, uEmail, uRole, uRestriction, uPhone, uISverified, uNotes, uDetails, uOrg,  uExternalID):
    print uName+","+uEmail+","+uRole+","+uRestriction+","+uPhone+","+uISverified+","+uNotes+","+uDetails
    
    h= httplib2.Http(".cache")
    h.add_credentials('user@email.com', 'Password')
    #setting verified to false because if true you have to send a password
    resp, content = h.request("http://sandbox1284059247.zendesk.com/users.xml", "POST",  body="<user>\
    <name>"+uName+"</name>\
    <restriction-id>"+uRestriction+"</restriction-id>\
    <roles>"+uRole+"</roles>\
    <email>"+uEmail+"</email>\
    <organization-id type=\"integer\">"+uOrg+"</organization-id>\
    <phone>"+uPhone+"</phone>\
    <notes>"+uNotes+"</notes>\
    <details>"+uDetails+"</details>\
    <is-verified type=\"boolean\">false</is-verified>\
    <external-id>"+uExternalID+"</external-id>\
    </user>",
    headers={'content-type' : 'application/xml'} )
    print content
    print resp
    if resp['status'] == '201':
        locationID = urlparse(resp['location'])
        #print locationID.path
        (dirName,  newID) = os.path.split(locationID.path)
        (unewID,  pathExt) = os.path.splitext(newID)
        print unewID+" created"
        return unewID
    elif resp['status'] == '406':
        unewID = getExistingUserID(uEmail)
        print unewID+" found in system"
        return unewID
    #print unewID



f2.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<users-conv>\n")

#goes through the users.xml file one user record at a time and pulls the data that can use used to create a new user out. 
for event, node in doc:
    if event == pulldom.START_ELEMENT and node.localName == "user":
        doc.expandNode(node) 
        userIDold = node.getElementsByTagName("id")
        UseridOld= str(userIDold[0].firstChild.data)
        print UseridOld + " old user id in main"

        userName = node.getElementsByTagName("name")
        Username= str(userName[0].firstChild.data)
        
        userRestrID = node.getElementsByTagName("restriction-id")
        UserrestrID= str(userRestrID[0].firstChild.data)
       
        userRoles = node.getElementsByTagName("roles")
        Userroles= str(userRoles[0].firstChild.data)
        
        userEmail = node.getElementsByTagName("email")
        Useremail = str(userEmail[0].firstChild.data)
       
        userOrgID = node.getElementsByTagName("organization-id")
        if userOrgID[0].firstChild != None:
            Userorg = str(userOrgID[0].firstChild.data)
            newID = orgIDcompare(Userorg)
        else: 
            newID = ""
       
        userPhone = node.getElementsByTagName("phone")
        if userPhone[0].firstChild != None:
            Userphone = str(userPhone[0].firstChild.data)
        else: 
            Userphone = ""
        userNotes = node.getElementsByTagName("notes")
        if userNotes[0].firstChild != None:
            Usernotes = str(userNotes[0].firstChild.data)
        else: 
            Usernotes = ""
        userDetails = node.getElementsByTagName("details")
        if userDetails[0].firstChild != None:
            Userdetails = str(userDetails[0].firstChild.data)
        else: 
            Userdetails = ""
        userVerifed = node.getElementsByTagName("is-verified")
        Userverifed= str(userVerifed[0].firstChild.data)
        userExtID = node.getElementsByTagName("external-id")
        if userExtID[0].firstChild != None:
            UserextID = str(userExtID[0].firstChild.data)
        else: 
            UserextID  = ""
        
        print userIDold[0].firstChild.data + " "+ userName[0].firstChild.data+" "+newID
        NewuserID = createUserZendesk (Username, Useremail, Userroles, UserrestrID, Userphone, Userverifed, Usernotes, Userdetails, newID,  UserextID)
        print NewuserID+" just befor the file write"
        print "<user>\n<old-user>"+ UseridOld+"</old-user>\n<new-user>"+NewuserID+"</new-user>\n</user>\n"
        #writes the old user ID and new user ID to a XML file that can be used later for example importing  tickets 
        f2.write("<user>\n<old-user>"+ UseridOld+"</old-user>\n<new-user>"+NewuserID+"</new-user>\n</user>\n")
f2.write("</users-conv>")
f2.close()

