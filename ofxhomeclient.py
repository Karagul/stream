#! /usr/bin/env python
import requests
from defusedxml.ElementTree import fromstring

class OFXHomeClient:
    def __init__(self):
        self.url = 'http://www.ofxhome.com/api.php'
        self.encoding = 'utf-8'

    ''' Due to the nature of the ofxhome query api, you cannot chain payload queries
    so there is no need to input a list of any kind
    '''
    def query(self, query='', term='', debug=False):
        # p = {}
        # p[str(query)] = str(term)
        r = requests.get(self.url, params={query,term})
        r.encoding = self.encoding
        if debug:
            print r.url
            print r.text
        return r

    ''' Retrieves the required ID based off of the institution  name.
    Since you can get many institutions, name is expected to be a list
    of strings and a dict of key=name value=id composition is returned
    '''
    def query_id(self, name=''):
        r = self.query('search', str(name))
        et = fromstring(str(r.content))
        return str(et.find('institutionid').get('id'))

    ''' Gets institution data and returns it as a dict.
    If brokerid is present, it is included in the dict, otherwise it
    is excluded.
    '''
    def query_institution(self, name=''):
        inst_id = self.query_id(str(name))
        r = self.query('lookup', str(inst_id))
        et = fromstring(str(r.content))

        # finally, the data we were looking for
        if et.find('brokerid') != None:
            return {'fid'      : et.find('fid').text,
                    'org'      : et.find('org').text,
                    'url'      : et.find('url').text,
                    'brokerid' : et.find('brokerid').text }
        else:
            return {'fid'      : et.find('fid').text,
                    'org'      : et.find('org').text,
                    'url'      : et.find('url').text }

#--- END OXFHomeClient Class -------------------------------------------#

def generate_config(name=''):
    oxf = OFXHomeClient()
    return oxf.query_institution(str(name))
