#! /usr/env/bin python

''' A tiny utility for building arbitrary XML tags, taken from oxf.py
found at http://stuffbillhasdone.blogspot.com/2010/04/ofx-python.html,
originally from http://www.jongsma.org/ofx/ (no longer available)
'''

join=str.join

def field(tag,value):
    return "<"+tag+">"+value

def tag(tag, *contents):
    return join("\r\n",["<"+tag+">"]+list(contents)+["</"+tag+">"])
