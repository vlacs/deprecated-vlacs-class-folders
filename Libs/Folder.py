__author__ = 'mgeorge@vlacs.org (Mike George)'

import json

import Database
import Utilities
import gdata.docs.client
import gdata.docs.data

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

def copy(client, folder_res_id, copy_to_res_id):
    copy_folder = client.GetResourceById(folder_res_id)
    copy_to_folder = client.GetResourceById(copy_to_res_id)

    folder = client.MoveResource(copy_folder, copy_to_folder, True)

    return folder.resource_id.text

def list_sub_folders(client, parent):
    sub_folder_list = {}

    uri = "/feeds/default/private/full/%s/contents/-/folder" % (parent)
    for resource in client.GetAllResources(uri=uri, show_root=True):
        sub_folder_list[resource.title.text] = resource.resource_id.text

    return sub_folder_list
