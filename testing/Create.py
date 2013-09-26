#Contains methods that are used by multiple tests

__author__ = 'mgeorge@vlacs.org (Mike George)'

import gdata.docs.client
import gdata.docs.data
import config

#Create Google Client Object
def Client(password):
    #Initialize Client Object
    client = gdata.docs.client.DocsClient(source=config.APP_NAME)
    
    #Toggle HTTP Debugging based on config
    client.http_client.debug = config.DEBUG
    
    #Attempt to login with supplied information, catch and notify on failure
    try:
        client.ClientLogin(email=config.USERNAME, password=password, source=config.APP_NAME)
    except gdata.client.BadAuthentication:
        exit('Invalid user credentials given.')
    except gdata.client.Error:
        exit('Login Error')
    
    return client

#Create an empty folder in Google Drive
def Folder(client, title, collection=None):
    #Initialize folder object with title
    folder = gdata.docs.data.Resource(type='folder', title=title)

    if collection != None:
        collection = client.GetResourceById(collection)
    
    #Use the Client Object to create the folder in the root of their Drive or the collection specified.
    folder = client.CreateResource(folder, collection=collection )
    
    #On success notify user and output folder Title and Resource ID
    print 'Created Folder: ', folder.title.text, folder.resource_id.text
