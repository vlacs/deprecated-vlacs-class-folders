#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import gdata.data
import gdata.docs.client
import gdata.docs.data
import gdata.docs.service
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
