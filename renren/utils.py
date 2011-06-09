#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def import_simplejson():
    try:
        import simplejson as json
    except ImportError:
        try:
            import json  # Python 2.6+
        except ImportError:
            try:
                from django.utils import simplejson as json  # GAE
            except ImportError:
                raise ImportError("Can't load a json library")
    return json



def parse_json(payload, encoding='ascii'):
    json = import_simplejson()
    if isinstance(payload, bytes):
        payload = payload.decode(encoding)
    return json.loads(payload)

def timestamp():
    return int(time.time())

def to_utf8(s):
    """ to utf8 str """
    if isinstance(s, str):
        s = s.encode('utf-8')
        # pass to next or last
    if isinstance(s, bytes):
        if not hasattr(s, 'encode'):
            return s.decode('ascii')
    elif isinstance(s, (list,tuple)):
        return ','.join(map(to_utf8, s))
    return str(s)
