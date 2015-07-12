#! /usr/bin/env python
import time
#import ofxhomeclient

from argparse import ArgumentParser as ap
from ofxclient import OFXClient as ofx
from lxml import etree as lxml

def main():
    args = parse_args()
    print args
    test(args.institution, args.user, args.passwd)

def test(inst, user, passwd):
    dtstart = time.strftime("%Y%m%d",time.localtime(time.time()-31*86400))
#    dtnow = time.strftime("%Y%m%d",time.localtime())
    client = ofx(inst, user, passwd)
    rawxml = client.query(qtype="account", dtstart=dtstart)
    print 'Printing raw XML'
    print rawxml
    print '\n\n'
    root = lxml.fromstring(rawxml)
    print (lxml.tostring(root, prettyprint=True))



def parse_args():
    p = ap(description="test OFX account query")
    p.add_argument('-i', '--institution',
                   action='store', type=str, required=True,
                   help='institution name, case insensitive')
    p.add_argument('-u', '--user',
                   action='store', type=str, required=True,
                   help='user name')
    p.add_argument('-p', '--passwd',
                   action='store', type=str, required=True,
                   help='user password')
    return p.parse_args()

if __name__ == '__main__':
    main()
