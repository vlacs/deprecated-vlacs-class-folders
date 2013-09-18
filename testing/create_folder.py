#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import os.path
import gdata.data
import gdata.acl.data
import gdata.docs.client
import gdata.docs.data
import gdata.docs.service
import gdata.sample_util
import getpass
import config

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
    CreateFolder(client, folder_name)
    
#Create an empty folder in Google Drive
def CreateFolder(client, title):
    folder = gdata.docs.data.Resource(type='folder', title=title)
    folder = client.CreateResource(folder, None, None, "/")
    print 'Created Folder: ', folder.title.text, collection.resource_id.text

if __name__ == '__main__':
    main()
