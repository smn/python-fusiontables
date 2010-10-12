#!/usr/bin/python
#
# Copyright (C) 2010 Google Inc.

""" ClientLogin.
"""

__author__ = 'kbrisbin@google.com (Kathryn Brisbin)'

import auth
import urllib, urllib2

class ClientLogin(auth.Authorization):
  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.auth_token = ""
    
    self.request_url = "http://www.google.com/fusiontables/api/query"
    
    self._authorize()
        
  def _authorize(self):
    auth_uri = 'https://www.google.com/accounts/ClientLogin'
    authreq_data = urllib.urlencode({
        'Email': self.username,
        'Passwd': self.password,
        'service': 'fusiontables',
        'accountType': 'HOSTED_OR_GOOGLE'})
    auth_req = urllib2.Request(auth_uri, data=authreq_data)
    auth_resp = urllib2.urlopen(auth_req)
    auth_resp_body = auth_resp.read()

    auth_resp_dict = dict(
        x.split('=') for x in auth_resp_body.split('\n') if x)
    self.auth_token = auth_resp_dict['Auth']
  
  def Get(self, query): 
    headers = {
      'Authorization': 'GoogleLogin auth=' + self.auth_token,
    }
    serv_req = urllib2.Request(url="%s?%s" % (self.request_url, query), 
                               headers=headers)
    serv_resp = urllib2.urlopen(serv_req)
    return serv_resp.read()
  
  def Post(self, query): 
    headers = {
      'Authorization': 'GoogleLogin auth=' + self.auth_token,
      'Content-Type': 'application/x-www-form-urlencoded',
    }

    serv_req = urllib2.Request(url=self.request_url, data=query, headers=headers)
    serv_resp = urllib2.urlopen(serv_req)
    return serv_resp.read()

  