__author__ = 'mgeorge@vlacs.org (Mike George)'

import json
import gdata.docs.client
import gdata.docs.data
import Utilities
import Database

#Create an empty folder in Google Drive
def create(conn, client, title, parent=None, class_id=None, noDB=False):
    #Initialize folder object with title
    folder = gdata.docs.data.Resource(type='folder', title=title)

    if parent != None:
        parent = client.GetResourceById(parent)

    #Use the Client Object to create the folder in the root of their Drive or the collection specified.
    folder = client.CreateResource(folder, collection=parent)

    if not noDB:
        if parent != None:
            Database.insert(conn, Database.structure_insert_string(Utilities.clean_title(title), folder.resource_id.text, parent.resource_id.text, class_id))
        else:
            Database.insert(conn, Database.structure_insert_string(Utilities.clean_title(title), folder.resource_id.text, parent, class_id))

    return folder

#Create an empty folder in Google Drive
def create_flat(conn, client, title, root_collection, parent=None, class_id=None, student_id=None):
    #Initialize folder object with title
    folder = gdata.docs.data.Resource(type='folder', title=title)

    if root_collection != None:
        root_collection = client.GetResourceById(root_collection)

    #Use the Client Object to create the folder in the root of their Drive or the collection specified.
    folder = client.CreateResource(folder, collection=root_collection)

    #On success insert into database
    Database.insert(conn, Database.structure_insert_string(Utilities.clean_title(title), folder.resource_id.text, parent, class_id, student_id))
 
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

        conn = Database.connect()
        #On success insert into database
        Database.insert("INSERT INTO vlacs_class_folders_shared (folder_id, shared_email, shared_permission) VALUES ('%s', '%s', '%s');" % (folder_res_id, share_with, permission))
        conn.close()

def unshare(client, folder_res_id, unshare_with):
    folder = client.GetResourceById(folder_id)
    acl_feed = client.GetAcl(folder)

    if len(acl_feed.entry) > 1:
        for e in acl_feed.entry:
            if e.scope.value == unshare_with:
                client.DeleteAclEntry(e)
                conn = Database.connect()
                Database.insert(conn, "DELETE FROM vlacs_class_folders_shared WHERE shared_email = ''" % (unshare_with))
                conn.close()

def copy(client, folder_res_id, copy_to_res_id):
    copy_folder = client.GetResourceById(folder_res_id)
    copy_to_folder = client.GetResourceById(copy_to_res_id)

    client.MoveResource(copy_folder, copy_to_folder, True)