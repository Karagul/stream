#! /usr/bin/env python
import time, os
import ofxhomeclient

from argparse import ArgumentParser as ap
from ofxclient import OFXClient as ofx

def main():
    args = parse_args()
    test(args.inst, args.user, args.passwd)

def test(inst, user, passwd):
    dtstart = time.strftime("%Y%m%d",time.localtime(time.time()-31*86400))
    dtnow = time.strftime("%Y%m%d",time.localtime())
    client = ofx(inst, user, passwd)
    print client.query(qtype="account", dtstart)


def parse_args():
    p = ap(decription="test OFX account query")
    p.add_argument('-i', '--institution', dest='inst',
                   action='store', type=str, required=True,
                   help='institution name, case insensitive')
    p.add_argument('-u', '--user', dest='user',
                   action='store', type=str, required=True,
                   help='account name')
    p.add_argument('-p', '--pass', dest='passwd',
                   action=GetPassAction, type=str, required=True,
                   help='account name')
    return p.parse_args()

class GetPassAction(ap.Action):
    def __init__(self,
             option_strings,
             dest=None,
             nargs=0,
             default=None,
             required=False,
             type=None,
             metavar=None,
             help=None):
        super(GetPassAction, self).__init__(
                option_strings=option_strings,
                dest=dest,
                nargs=nargs,
                default=default,
                required=required,
                metavar=metavar,
                type=type,
                help=help)

if __name__ == '__main__':
    main()
