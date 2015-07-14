# -*- coding: utf-8 -*-
'''
    finance.ofxhomeclient
    ~~~~~~~~~~~~~~~~~~~~~

    ofxhomeclient provides utility functions for interacting with the
    www.ofxhome.com web API.

    :copyright: (c) 2015 by Calvin Maguranis.
    :license: BSD, see LICENSE for more details.
'''

import requests
from defusedxml.ElementTree import fromstring

''' Due to the nature of the ofxhome query api, you cannot chain payload
queries so there is no need to input a list of any kind.
'''
def query(query='', term='', debug=False):
    url = 'http://www.ofxhome.com/api.php'
    encoding = 'utf-8'

    r = requests.get(url, params={query : term})
    r.encoding = encoding
    if debug:
        print r.url
        print r.text
    return r

''' Retrieves the required ID based off of the institution  name.
Since you can get many institutions, name is expected to be a list
of strings and a dict of key=name value=id composition is returned
'''
def query_id(name=''):
    r = query('search', str(name))
    et = fromstring(str(r.content))
    return str(et.find('institutionid').get('id'))

''' Gets institution data and returns it as a dict.
If brokerid is present, it is included in the dict, otherwise it
is excluded.
'''
def query_institution(name=''):
    inst_id = query_id(str(name))
    r = query('lookup', str(inst_id))
    et = fromstring(str(r.content))

    # finally, the data we were looking for
    if et.find('brokerid') != None:
        return {'fid'      : et.find('fid').text,
                'fiorg'    : et.find('org').text,
                'url'      : et.find('url').text,
                'brokerid' : et.find('brokerid').text }
    else:
        return {'fid'      : et.find('fid').text,
                'fiorg'    : et.find('org').text,
                'url'      : et.find('url').text }
