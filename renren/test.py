#!/usr/bin/env python
# -*- coding: utf-8 -*-


import oauth2 as oauth
import webbrowser

# http://app.renren.com/developers/app/112893

API_Id = 'b3e99c82722f4204a43cf94129caf8e0'
API_Secret = 'e17954ec48cb4aa085144402f2604ff5'

"""
REQUEST_TOKEN_URL = 'https://photos.example.net/request_token'
ACCESS_TOKEN_URL = 'https://graph.renren.com/oauth/token'
AUTHORIZATION_URL = "https://graph.renren.com/oauth/authorize"

BASE_URL = "https://graph.renren.com/oauth/"

"""
CALLBACK_URL = "http://graph.renren.com/oauth/login_success.html"
#class RenrenOAuthClient(oauth.Client2):
from auth import AuthHandler
from api import API
auth = AuthHandler(API_Id, API_Secret, CALLBACK_URL)




raise SystemExit

#url = auth.get_authorization_url()

#webbrowser.open(url)

#code='O3guyRWG81z6ca4cjx5NIfXFx2elBCkd'
#code = raw_input('code:').strip()

#token = auth.get_access_token(code)
#print token

#token = token['access_token']

#session = auth.get_session_key(token)
#print session

#sessionKey = session["renren_token"]["session_key"]
sessionKey = "5.f0549d07725f8210991171a2e05c1067.86400.1302368400-319621581"

auth.set_session_key(sessionKey)

api = API(auth)
