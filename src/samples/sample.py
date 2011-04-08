'''
Created on Dec 21, 2010

@author: kbrisbin
'''


from ftclient import ClientLoginFTClient
from ftclient import OAuthFTClient
from authorization.oauth import OAuth
from authorization.clientlogin import ClientLogin
from sql.sqlbuilder import SQL


def clientlogin_example(username, password):
  clientlogin = ClientLogin()
  token = clientlogin.authorize(username, password)
  client = ClientLoginFTClient(token)
  print client.query(SQL().showTables())


def oauth_example(key, secret):
  oauthlogin = OAuth()
  url, oauth_token, oauth_token_secret = oauthlogin.generateAuthorizationURL(key, 
                                                                            secret, 
                                                                            key, 
                                                                            None)
  
  
  print url
  
  raw_input("hit enter")
  
  oauth_teokn, oauth_secret = oauthlogin.authorize(key, 
                                                   secret,
                       oauth_token, 
                       oauth_token_secret)
  
  client = OAuthFTClient(key, secret, oauth_teokn, oauth_secret)
  print client.query("SELECT * FROM 316962")

if __name__ == "__main__":
  oauth_example("consumerkey", "consumersecret")

