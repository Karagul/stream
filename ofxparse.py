# -*- coding: utf-8 -*-
'''
    finance.ofxparse
    ~~~~~~~~~~~~~~~~

    A small utility for parsing ofx data grams.

    :copyright: (c) 2015 by Calvin Maguranis.
    :license: BSD, see LICENSE for more details.
'''

''' Tree provides a tree representation of an OFX datagram.

Under the hood the tree is a list of lists
'''
class Tree():
    def __init__(self, strgram):
        self.strgram = strgram
        self.tree = []

    ''' Returns the name of the current element. '''
    def _get_name(self,string):
        if string is None: return None
        else:
            end = string.find('>')
            element = string[:end]
            return element.strip('<>/')

    ''' Parses the OFX datagram string and returns a python
    dictionary of the data.
    '''
    def _buildtree(self,datagram):
        pos = 0

# - End Tree Class -------------

''' Custom container for iterating over raw string OFX datagrams. '''
class DatagramIter():
    def __init__(self,datagram):
        self.strgram = str(datagram)
        self.length = len(self.strgram)
        self.pos=0

    def __iter__(self): return self

    def next(self):
        concat = self.strgram[self.pos:]
        if self.pos >= self.length or concat.find('<') < 0:
            raise StopIteration
        else:
            start = concat.find('<')
            # only if start is not 0 we need to increase the value
            if start > 0: start += 1
            elif start < 0: raise StopIteration

            end = concat[start+1:].find('<')
            if end < 0:
                element = concat[start:]
                end = self.length
            else: element = concat[start:end + 1]

            self.pos = (self.pos + end + 1)
            return element

# - End DatagramIter Class -------------

if __name__ == '__main__':
    dgstr = '<OFX><SIGNONMSGSRSV1><SONRS><STATUS><CODE>0<SEVERITY>INFO<MESSAGE>Success</STATUS><DTSERVER>20150714184633<LANGUAGE>ENG<FI><ORG>USAA<FID>24591</FI></SONRS></SIGNONMSGSRSV1><SIGNUPMSGSRSV1><ACCTINFOTRNRS><TRNUID>59D885C2-D259-4E1D-B88A-71CDDC025117<STATUS><CODE>0<SEVERITY>INFO<MESSAGE>Success</STATUS><CLTCOOKIE>4<ACCTINFORS><DTACCTUP>20150714120000<ACCTINFO><DESC>USAA SECURE CHECKING<BANKACCTINFO><BANKACCTFROM><BANKID>314074269<ACCTID>0051690446<ACCTTYPE>CHECKING</BANKACCTFROM><SUPTXDL>Y<XFERSRC>N<XFERDEST>N<SVCSTATUS>ACTIVE</BANKACCTINFO></ACCTINFO>'
    parse = OFXDatagramIter(dgstr)
    count = 0
    for element in parse:
        print element
