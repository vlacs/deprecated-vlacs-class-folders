#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import gdata.docs.client
import gdata.docs.data
import gdata.docs.service
import getpass
import config

#Global Variables
password = ""

#Main Method
def main():
    client = gdata.docs.service.DocsService()
    folder_name = ""

    print "Welcome, Please enter your password: "
    password = getpass.getpass()

    client.ClientLogin(config.username, password)
    client = gdata.docs.client.DocsClient(client)

    print "What would you like to name your folder?: "
    raw_input(folder_name)

    print "Creating a new folder..."
    CreateCollection(client, folder_name)
    
#Create an empty folder in Google Drive
def CreateCollection(client, title):
    collection = gdata.docs.data.Resource(type='folder', title=title)
    collection = client.CreateResource(collection)
    print 'Created Collection: ', collection.title.text, collection.resource_id.text

if __name__ == '__main__':
    main()
