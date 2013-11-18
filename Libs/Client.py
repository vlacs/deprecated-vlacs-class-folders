__author__ = 'mgeorge@vlacs.org (Mike George)'

from Config import config
import gdata.docs.client
import gdata.docs.data

#Create Google Client Object
def create():
    #Initialize Client Object
    client = gdata.docs.client.DocsClient(source=config.APP_NAME)

    #Toggle HTTP Debugging based on config
    client.http_client.debug = config.DEBUG

    #Attempt to login with supplied information, catch and notify on failure
    try:
        client.ClientLogin(email=config.USERNAME, password=config.PASSWORD, source=config.APP_NAME)
    except gdata.client.BadAuthentication:
        exit('Invalid user credentials given.')
    except gdata.client.Error:
        exit('Login Error')

    return client
