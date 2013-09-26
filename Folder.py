__author__ = 'mgeorge@vlacs.org (Mike George)'

import gdata.docs.client
import gdata.docs.data

#Create an empty folder in Google Drive
def create(client, title, collection=None):
    #Initialize folder object with title
    folder = gdata.docs.data.Resource(type='folder', title=title)

    if collection != None:
        collection = client.GetResourceById(collection)
    
    #Use the Client Object to create the folder in the root of their Drive or the collection specified.
    folder = client.CreateResource(folder, collection=collection)
    
    #On success notify user and output folder Title and Resource ID
    print 'Created Folder: ', folder.title.text, folder.resource_id.text

def share(client, folder_res_id, share_with, permission='writer'):
	folder = client.get_resource_by_id(folder_res_id)
    
    acl_entry = gdata.docs.data.AclEntry(
        scope=gdata.acl.data.AclScope(value=share_with, type='user'),
        role=gdata.acl.data.AclRole(value=permission),
    )

    client.AddAclEntry(folder, acl_entry, send_notifications=False)

def unshare(client, folder_res_id):
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