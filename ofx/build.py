# -*- coding: utf-8 -*-
'''
    finance.ofx.build
    ~~~~~~~~~~~~~~~~~

    A tiny utility for building ofx data grams, taken from oxf.py
    found at http://stuffbillhasdone.blogspot.com/2010/04/ofx-python.html,
    originally from http://www.jongsma.org/ofx/ (no longer available).

    :copyright: (c) 2015 by Calvin Maguranis.
    :license: BSD, see LICENSE for more details.
'''

join = str.join

def field(tag,value):
    return '<'+tag+'>'+value

def tag(tag, *contents):
    return join('\r\n',['<'+tag+'>']+list(contents)+['</'+tag+'>'])
