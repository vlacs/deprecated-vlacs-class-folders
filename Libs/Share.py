#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

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

        conn = Database.connect()
        #On success insert into database
        Database.insert("INSERT INTO vlacs_class_folders_shared (folder_id, shared_email, shared_permission) VALUES ('%s', '%s', '%s');" % (folder_res_id, share_with, permission))
        conn.close()

def create_share_structure():
	pass

def unshare():
	pass

def remove_share_structure():
	pass