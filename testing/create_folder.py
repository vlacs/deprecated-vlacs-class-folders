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
    folder_name = ""

    password = getpass.getpass("Welcome, Please enter your password: ")

    client = CreateClient(password)

    folder_name = raw_input("What would you like to name your folder?: ")

    print "Creating a new folder..."
    CreateFolder(client, folder_name)

#Create Google Client Object
def CreateClient(password):
    client = gdata.docs.client.DocsClient(source=config.APP_NAME)
    client.http_client.debug = config.DEBUG
    try:
        client.ClientLogin(email=config.USERNAME, password=password, source=config.APP_NAME)
    except gdata.client.BadAuthentication:
        exit('Invalid user credentials given.')
    except gdata.client.Error:
        exit('Login Error')
    
    return client

#Create an empty folder in Google Drive
def CreateFolder(client, title):
    folder = gdata.docs.data.Resource(type='folder', title=title)
    folder = client.CreateResource(folder)
    print 'Created Folder: ', folder.title.text, folder.resource_id.text

if __name__ == '__main__':
    main()
