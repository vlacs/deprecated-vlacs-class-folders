#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import Create
import getpass
import config

def main():
	#Prompt user to enter password
    password = getpass.getpass("Welcome, Please enter your password: ")
    
    #Create Client Object, Password required
    client = Create.Client(password)
    
    #Prompt user to enter folder name and the Resource ID of parent folder
    folder_name = raw_input("What would you like to name your folder?: ")
    parent_folder = raw_input("Please enter the Resource ID of the desired parent folder: ")
    
    #Let the user know then create the folder
    print "Creating a new subfolder..."
    Create.Folder(client, folder_name, parent_folder)

#Run Main method automatically
if __name__ == '__main__':
    main()