#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import gdata.data
import gdata.docs.data
import gdata.docs.service
import gdata.acl
import Create
import getpass
import config

#Main Method
def main():
    #Prompt user to enter password
    password = getpass.getpass("Welcome, Please enter your password: ")

    client = Create.Client(password)

    folder_res_id = raw_input("Enter the Resource ID of the folder you'd like to share: ")
    share_with = raw_input("Enter the email address that you'd like to share the folder with: ")

    print "Sharing Folder..."
    ShareFolder(client, folder_res_id, share_with)

#Share a folder with another Google Drive user
def ShareFolder(client, folder_res_id, share_with):
    folder = client.get_resource_by_id(folder_res_id)
    
    acl_entry = gdata.docs.data.AclEntry(
        scope=gdata.acl.data.AclScope(value=share_with, type='user'),
        role=gdata.acl.data.AclRole(value='writer'),
    )

    client.AddAclEntry(folder, acl_entry, send_notification=False)

#Run Main method automatically
if __name__ == '__main__':
    main()
