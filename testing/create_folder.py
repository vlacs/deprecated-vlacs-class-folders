#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

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
    Create.Folder(client, folder_name)

#Run Main method automatically
if __name__ == '__main__':
    main()
