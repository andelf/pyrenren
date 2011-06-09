#!/usr/bin/env python
# -*- coding: utf-8 -*-


# http://app.renren.com/developers/app/112893

from .utils import timestamp, parse_json


class API(object):
    """API class"""
    API_URI = "http://api.renren.com/restserver.do"
    def __init__(self, auth):
        self._auth = auth
        self.http = auth.http

    # http://wiki.dev.renren.com/wiki/API
    def call(self, method=None, **kwargs):
        args = dict(
            method = method or 'users.getLoggedInUser',
            )
        args.update(kwargs)
        return self.request(args)

    def request(self, args):
        uri = self.API_URI
        # signed_urlencode will auto add format
        body = self._auth.signed_urlencode(args)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response, content = self.http.request(uri, method='POST',
                                              body=body,
                                              headers=headers)
        content = parse_json(content, 'utf-8')
        return content

    def requestMultipart(self, filename, contentname='upload', **kwargs):
        # TODO: implement me
        pass
