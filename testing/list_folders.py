#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import getpass
import Create
import gdata.data
import gdata.acl.data
import gdata.docs.client
import gdata.docs.data

def main():
    password = getpass.getpass("Welcome, Please enter your password: ")

    client = Create.Client(password)
    
    print "Retrieving a list of top level folders..."
    feed = client.GetResources(uri='/feeds/default/private/full/folder%3Aroot/contents/-/folder')
    PrintFeed(feed)

def PrintFeed(feed):
    for entry in feed.entry:
        print entry.resource_id.text, entry.title.text

if __name__ == '__main__':
    main()
