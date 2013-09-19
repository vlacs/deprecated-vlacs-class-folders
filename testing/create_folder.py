#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import gdata.data
import gdata.docs.client
import gdata.docs.data
import gdata.docs.service
import getpass
import Create
import config

#Main Method
def main():
    #Prompt user to enter password
    password = getpass.getpass("Welcome, Please enter your password: ")
    
    #Create Client Object, Password required
    client = Create.Client(password)
    
    #Prompt user to enter folder name
    folder_name = raw_input("What would you like to name your folder?: ")
    
    #Let the user know then create the folder
    print "Creating a new folder..."
    CreateFolder(client, folder_name)

#Create an empty folder in Google Drive
def CreateFolder(client, title):
    #Initialize folder object with title
    folder = gdata.docs.data.Resource(type='folder', title=title)
    
    #Use the Client Object to create the folder in the root of their Drive
    folder = client.CreateResource(folder)
    
    #On success notify user and output folder Title and Resource ID
    print 'Created Folder: ', folder.title.text, folder.resource_id.text

#Run Main method automatically
if __name__ == '__main__':
    main()
