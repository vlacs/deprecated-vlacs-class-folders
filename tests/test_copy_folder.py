#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import sys
from Libs import Client
from Libs import Folder

def main(folder, copy_to_folder):
    client = Client.create()
    print("Moving folder %s to %s" % (folder, copy_to_folder))
    Folder.copy(client, folder, copy_to_folder)
    print("Done!")
    

# TODO: consider getopt() for make benefit glorious CLI
if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])