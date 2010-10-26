#!/usr/bin/python
#
# Copyright (C) 2010 Google Inc.

""" OAuth Login.

Uses python-oauth2 library to perform 3-way handshake.

1. Create a new instance OAuth
2. Call the generateAuthorizationURL method to create
the authorization URL
3. Once the user grants access
4. Call the authorize method to upgrade to an access
token.
"""

__author__ = 'kbrisbin@google.com (Kathryn Brisbin)'

import oauth2
import urlparse


class OAuth():
  scope = "http://www.google.com/fusiontables/api/query"

  def __init__(self, consumer_key, consumer_secret, domain):
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.domain = domain

    self.request_token_url = "https://www.google.com/accounts/OAuthGetRequestToken"
    self.access_token_url = 'https://www.google.com/accounts/OAuthGetAccessToken'
    self.authorize_url = 'https://www.google.com/accounts/OAuthAuthorizeToken'

    self.consumer = None
    self.request_token = None
    self.client = None


  def generateAuthorizationURL(self):
    """ Fetch the OAuthToken and generate the authorization URL.
    Returns:
      the Authorization URL
    """
    self.consumer = oauth2.Consumer(self.consumer_key, self.consumer_secret)
    client = oauth2.Client(self.consumer)

    resp, content = client.request("%s?scope=%s" % (self.request_token_url, OAuth.scope), "GET")
    if resp['status'] != '200': raise Exception("Invalid response %s." % resp['status'])

    self.request_token = dict(urlparse.parse_qsl(content))

    return "%s?oauth_token=%s&scope=%s&domain=%s" % (self.authorize_url,
                                                     self.request_token['oauth_token'],
                                                     OAuth.scope,
                                                     self.domain)


  def authorize(self):
    """ Upgrade OAuth to Access Token
    Returns:
      the oauth token
      the token secret
    """
    token = oauth2.Token(self.request_token['oauth_token'], self.request_token['oauth_token_secret'])
    client = oauth2.Client(self.consumer, token)

    resp, content = client.request(self.access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))
    return access_token['oauth_token'], access_token['oauth_token_secret']


