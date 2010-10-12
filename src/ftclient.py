#!/usr/bin/python
#
# Copyright (C) 2010 Google Inc.

""" Fusion Tables Client.

Issue requests to Fusion Tables.
"""

__author__ = 'kbrisbin@google.com (Kathryn Brisbin)'


import urllib

class FTClient():
  
  def __init__(self, auth_client):
    self.auth_client = auth_client

  def query(self, query, request_type=None):
    """ Issue a query to the Fusion Tables API and return the result. """
    lowercase_query = query.lower()
    if lowercase_query.startswith("select") or \
       lowercase_query.startswith("describe") or \
       lowercase_query.startswith("show") or \
       request_type=="GET":
      
      return self.auth_client.Get(urllib.urlencode({'sql': query}))
    
    else:
      return self.auth_client.Post(urllib.urlencode({'sql': query}))

