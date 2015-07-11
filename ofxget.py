#! /usr/bin/env python

import requests

def is_int(x):
    try:
        return (int(x) > 0)
    except ValueError:
        return False

''' Due to the nature of the ofxhome query api, you cannot chain payload queries
 so there is no need to input a list of any kind
'''
def query_ofxhome_api(query="", term=""):
    url = "http://www.ofxhome.com/api.php"
    p = {}
    p[str(query)] = str(term)
    r = requests.get(url, params=p)
    r.encoding = "utf-8"
    print r.url
    print r.text
    return r
