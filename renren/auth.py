#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import oauth2 as oauth
from .utils import parse_json, to_utf8, timestamp
from .compat import urlencode

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

class AuthHandler(object):

    BASE_URL = "https://graph.renren.com/oauth/"
    RENREN_SESSION_KEY_URI = "https://graph.renren.com/renren_api/session_key"

    def __init__(self, API_Key, API_Secret, callback=None, scope=None):

        self.callback = callback
        self._oauth = oauth.Client2(API_Key, API_Secret, self.BASE_URL,
                                   redirect_uri=callback)
        self.http = self._oauth.http

        self.secret = API_Secret

        self.apiKey = API_Key
        self.sessionKey = None

        self.params = {}
        if scope:
            self.params['scope'] = scope

    def get_authorization_url(self):
        redirect_uri = self.callback
        params = self.params
        return self._oauth.authorization_url(redirect_uri, params)

    def get_access_token(self, code):
        redirect_uri = self.callback
        params = self.params
        return self._oauth.access_token(code, redirect_uri, params)

    def get_session_key(self, access_token):
        args = dict(oauth_token = access_token)
        if self.params:
            args.update(self.params)

        uri = self.RENREN_SESSION_KEY_URI
        body = urlencode(args)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response, content = self.http.request(uri, method='POST',
                                              body=body,
                                              headers=headers)
        if response.status != 200:
            raise Exception(content)

        try:
            session = parse_json(content)
            self.sessionKey = session["renren_token"]["session_key"]
            return session
        except Exception as e:
            raise Exception(e)

    def set_session_key(self, session_key):
        self.sessionKey = session_key

    def signed_urlencode(self, query):
        query = dict(query)
        if "session_key" not in query:
            query["session_key"] = self.sessionKey
        if "api_key" not in query:
            query["api_key"] = self.apiKey
        if "call_id" not in query:
            query["call_id"] = timestamp()
        if "v" not in query:
            query["v"] = "1.0"
        if "format" not in query:
            query['format'] = "JSON"

        query = query.items()
        query = [(k, to_utf8(v)) for k,v in query]
        query.sort()

        params = ''.join(("%s=%s" % kv) for kv in query)
        params += self.secret
        sig = md5(params.encode('utf-8')).hexdigest()
        return urlencode(query) + "&sig=" + sig


