# -*- coding: ascii -*-
#--------------------------------------------------------------
#Created on Nov 11, 2013
#
#@author: Piyush Harsh
#@contact: piyush.harsh@zhaw.ch
#@organization: ICCLab, Zurich University of Applied Sciences
#@summary: Module to interact with OS-keystone service
#@var username, tenant-id, password
#@requires: python 2.7
#--------------------------------------------------------------


import httplib2 as http
import sys, re
import json
import getpass

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
    
def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def login():
    user = raw_input("Username [%s]: " % getpass.getuser())
    tenant = raw_input("Tenant Id: ")
    if not user:
        user = getpass.getuser()
    pprompt = lambda: (getpass.getpass())
    p1 = pprompt()
    return user, p1, tenant

def get_endpoints(tokenId, uri):
    headers = {
               'Accept': 'application/json',
               'Content-Type': 'application/json;'
    }
    # uri = 'http://160.85.4.11:5000' #replace this with the API end-point of your setup
    path = '/v2.0/tokens/' + tokenId + '/endpoints'
    target = urlparse(uri+path)
    method = 'GET'
    body = ''
    h = http.Http()
    response, content = h.request(target.geturl(),method,body,headers)
    print "Endpoints:\n" + content

#TODO: write the get token method with API v3    
def get_token_v3():
    headers = {
               'Accept': 'application/json',
               'Content-Type': 'application/json;'
    }
    
def get_token_v2(uri):
    auth_data = {}     #an empty dictionary
    headers = {
               'Accept': 'application/json',
               'Content-Type': 'application/json;'
    }
    
    path = '/v2.0/tokens'
    target = urlparse(uri+path)
    method = 'POST'
    username, password, tenant = login()
    #defining the request body here
    body = '{"auth":{"passwordCredentials":{"username": "' + username + '", "password": "' + password + '"},"tenantId":"' + tenant + '"}}'
    
    h = http.Http()
    response, content = h.request(target.geturl(),method,body,headers)
    #converting the header of the response to json object
    header = json.dumps(response)
    json_header = json.loads(header)
    
    server_response = json_header["status"]
    auth_data["server-response"] = server_response
    if server_response not in {'200'}:
        print "Inside get_token_v2(): Something went wrong!"
        return False, auth_data
    else:
        data = json.loads(content)
        auth_data["token-issued-at"] = data["access"]["token"]["issued_at"]
        auth_data["token-expires-at"] = data["access"]["token"]["expires"]
        auth_data["token-id"] = data["access"]["token"]["id"]
        auth_data["user-name"] = data["access"]["user"]["username"]
        auth_data["user-id"] = data["access"]["user"]["id"]
        for i in range(len(data["access"]["serviceCatalog"])):
            catalog_element =  data["access"]["serviceCatalog"][i]
            #print catalog_element["name"] + ", " + catalog_element["type"] + ", endpoint: " + catalog_element["endpoints"][0]["publicURL"]
            auth_data[catalog_element["name"]] = catalog_element["endpoints"][0]["publicURL"]
    return True, auth_data 

#a simple API test case with nova
def get_server_list(token, api_endpoint):
    headers = {
               'Accept': 'application/json',
               'Content-Type': 'application/json;',
               'X-Auth-Token': token
    }
    path = "/servers"
    target = urlparse(api_endpoint+path)
    method = 'GET'
    body = ''
    h = http.Http()
    response, content = h.request(target.geturl(),method,body,headers)
    #converting the header of the response to json object
    header = json.dumps(response)
    json_header = json.loads(header)
    
    server_response = json_header["status"]
    if server_response not in {'200'}:
        print "Inside get_server_list(): Something went wrong!"
        return False, server_list
    else:
        data = json.loads(content)
        servers = data["servers"]
        server_list = [None] * len(servers)   #create an array to hold parsed data
        for i in range(len(servers)):
            server_list[i] = {}
            server_list[i]["id"] = servers[i]["id"]
            server_list[i]["name"] = servers[i]["name"]
            server_list[i]["url"] = servers[i]["links"][0]["href"]
    return True, server_list
        
def main(argv):
    print "Hello There. This is a simple test application making a test API call to OpenStack"
    #auth_uri = 'http://192.168.100.51:5000' #internal test-setup, replace it with your own value
    auth_uri = 'http://160.85.4.11:5000' #internal test-setup, replace it with your own value
    status, token_data = get_token_v2(auth_uri)
    if status:
        for key, value in token_data.iteritems():
            print key, value
    else:
        print "Authentication was not successful."
    if status:
        status, server_list = get_server_list(token_data["token-id"], token_data["nova"])
        if status:
            print "The list of servers are printed next."
            print server_list
    return True
    
if __name__ == '__main__':
    main(sys.argv[1:])