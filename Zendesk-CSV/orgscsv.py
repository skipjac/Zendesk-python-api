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
#doc = pulldom.parse("skipjack-20110609/organizations.xml")

def convertOrgCSV(doc):
    #this is were the look XML is written 
    f2 = open('orgs.csv',  'w')
    f2.write("name,notes,details,is-shared,is-shared-comments,group-id,domain-map\n")

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
            else: 
                newID = ""
            
            
            orgDefaultold = node.getElementsByTagName("default")
            if orgDefaultold[0].firstChild != None:
                Orgdefault= str(orgDefaultold[0].firstChild.data)
            else: 
                Orgdefault = ""
           
            
            #writes the old org ID with the new org ID 
            f2.write(Orgname+","+Orgnotes+","+Orgdetails+","+Orgshared+","+Orgscomment+","+Groupid+","+Orgdefault+"\n")
            print orgIDold[0].firstChild.data + " "+Orgname+","+Orgnotes+","+Orgdetails+","+Orgshared+","+Orgscomment+","+Groupid+","+Orgdefault+"\n"
    f2.close()

if (sys.argv[1] > 1):
    doc = pulldom.parse(sys.argv[1])
    convertOrgCSV(doc)
else:
    print("you need to provide a file ")
