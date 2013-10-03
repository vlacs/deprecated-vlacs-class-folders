__author__ = 'mgeorge@vlacs.org (Mike George)'

import json
import gdata.docs.client
import gdata.docs.data
from Utilities import Clean
import Database

#Create an empty folder in Google Drive
def create(client, title, parent=None, class_id=None):
    #Initialize folder object with title
    folder = gdata.docs.data.Resource(type='folder', title=title)

    if parent != None:
        parent = client.GetResourceById(parent)
    
    #Use the Client Object to create the folder in the root of their Drive or the collection specified.
    folder = client.CreateResource(folder, collection=parent)
    
    #On success insert into database
    if parent != None and class_id != None:
        Database.execute("INSERT INTO vlacs_class_folders_structure (class_id, folder_name, folder_id, folder_parent) VALUES ('%s', '%s', '%s', '%s');" % (class_id, Clean.title(title), folder.resource_id.text, parent.resource_id.text))
    elif parent != None:
        Database.execute("INSERT INTO vlacs_class_folders_structure (folder_name, folder_id, folder_parent) VALUES ('%s', '%s', '%s');" % (Clean.title(title), folder.resource_id.text, parent.resource_id.text))
    else:
        Database.execute("INSERT INTO vlacs_class_folders_structure (folder_name, folder_id) VALUES ('%s', '%s');" % (Clean.title(title), folder.resource_id.text))

    return folder

def share(client, folder_res_id, share_with, permission='writer'):
	#Check if already shared with person
    result = Database.get(query="SELECT shared_email FROM vlacs_class_folders_shared WHERE shared_email = '%s';" % (share_with))

    if len(result['cursor']) < 1:
        folder = client.get_resource_by_id(folder_res_id)
        
        acl_entry = gdata.docs.data.AclEntry(
            scope=gdata.acl.data.AclScope(value=share_with, type='user'),
            role=gdata.acl.data.AclRole(value=permission),
        )

        client.AddAclEntry(folder, acl_entry, send_notifications=False)

        #On success insert into database
        Database.execute("INSERT INTO vlacs_class_folders_shared (folder_id, shared_email, shared_permission) VALUES ('%s', '%s', '%s');" % (folder_res_id, share_with, permission))

def unshare(client, folder_res_id, unshare_with):
	folder = client.GetResourceById(folder_id)
	acl_feed = client.GetAcl(folder)

	if len(acl_feed.entry) > 1:
		for e in acl_feed.entry:
			if e.scope.value == unshare_with:
				client.DeleteAclEntry(e)
				Database.execute("DELETE FROM vlacs_class_folders_shared WHERE shared_email = ''" % (unshare_with))