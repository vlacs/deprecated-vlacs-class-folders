#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from Libs import Client
import gdata.data
import gdata.docs.client
import gdata.docs.data

def main():
	client = Client.create()

	#folder_count = get_resources('folder:0B7AqvGrb_oO8SDYwem5zcTdrMnM', client)
	folder_count = get_resources('root', client)

	print "Done!"

def get_resources(collection_id, client, recursed=False):
	for resource in client.GetAllResources(uri="/feeds/default/private/full/%s/contents/-/folder" % collection_id, show_root=True):
		print resource.title.text, '|', resource.resource_id.text, '|', resource.GetResourceType(), '| Parent:', collection_id, '| Recursed: ' + str(recursed)
		if resource.GetResourceType() == 'folder':
			if not recursed:
				count = get_resources(resource.resource_id.text, client, True)

if __name__ == "__main__":
	main()