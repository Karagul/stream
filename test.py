#! /usr/bin/env python

import requests
from defusedxml.ElementTree import parse, fromstring
from ofxget import query_ofxhome_api as query

def test():
    # get xml data
    r = query("search", "usaa")

    # parse it
    et = fromstring(str(r.content))
    id = str(et.find('id').text)
    print id


''' Retrieves the required ID based off of the institution  name.
Since you can get many institutions, name is expected to be a list
of strings and a dict of key=name value=id composition is returned
'''
def get_id(name=""):
    r = query("search", str(name))
    et=fromstring(str(r.content))
    return str(et.find('institutionid').get('id'))

def get_institution(name=""):
    id = get_id(str(name))
    r = query("lookup", str(id))
    et = fromstring(str(r.content))

    # finally, the data we were looking for
    fid = et.find("fid").text
    org = et.find("org").text
    url = et.find("url").text
