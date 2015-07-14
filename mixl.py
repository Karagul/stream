# -*- coding: utf-8 -*-
'''
    finance.mixl
    ~~~~~~~~~~~~~~~~~~~~~

    A tiny utility for building arbitrary XML tags, taken from oxf.py
    found at http://stuffbillhasdone.blogspot.com/2010/04/ofx-python.html,
    originally from http://www.jongsma.org/ofx/ (no longer available)

    TODO:
    - Add ability to parse OFX files
    - Probably should change name to something more descriptive...ofxparse,
    maybe?

    :copyright: (c) 2015 by Calvin Maguranis.
    :license: BSD, see LICENSE for more details.
'''

def field(tag,value):
    return '<'+tag+'>'+value

def tag(tag, *contents):
    return ''.join('\r\n',['<'+tag+'>']+list(contents)+['</'+tag+'>'])
