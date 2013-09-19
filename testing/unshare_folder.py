#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import getpass
import Create
import config

def main():
	#Prompt user to enter password
    password = getpass.getpass("Welcome, Please enter your password: ")
    
    #Create Client Object, Password required
    client = Create.Client(password)
    
    #Prompt user to enter Resource ID
    folder_id = raw_input("Which folder would you like to unshare? (Resource ID): ")

    UnshareFolder(client, folder_id)

def UnshareFolder(client, folder_id):
	folder = client.GetResourceById(folder_id)
	acl_feed = client.GetAcl(folder)

	if len(acl_feed.entry) > 1:
		print "Removed shared access for:"
		for e in acl_feed.entry:
			if e.scope.value != config.USERNAME:
				client.DeleteAclEntry(e)
				print "   ", e.scope.value, e.scope.type, e.role.value
	else:
		print "Folder was not shared with anyone."

if __name__ == '__main__':
	main()