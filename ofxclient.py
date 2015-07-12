#!/usr/bin/python
import time, os
import requests

from mixl import tag, field
from ofxhomeclient import generate_config as gencfg

join = str.join

def _date():
    return time.strftime('%Y%m%d%H%M%S',time.localtime())

def _genuuid():
    return os.popen('uuidgen').read().rstrip().upper()

'''
sites = {
    'MYCreditUnion': {
        'caps': [ 'SIGNON', 'BASTMT' ],
        'fid': '31337',     # ^- this is what i added, for checking/savings/debit accounts- think 'bank statement'
        'fiorg': 'MyCreditUnion',
        'url': 'https://ofx.mycreditunion.org',
        'bankid': '21325412453', # bank routing' #
        },
    'vanguard': {
        'caps': [ 'SIGNON', 'INVSTMT'],
        'fiorg': 'vanguard.com',
        'url' : 'https://vesnc.vanguard.com/us/OfxDirectConnectServlet',
        },
    'schwab_brokerage': {
        'caps': [ 'SIGNON', 'INVSTMT'],
        'fiorg': 'SCHWAB>COM',
        'url': 'https://ofx.schwab.com/cgi_dev/ofx_server',
        },
    'schwab_bank': {
        'caps': [ 'SIGNON', 'BASTMT'],
        'fid' : '101',
        'fiorg': 'ISC',
        'url': 'https://ofx.schwab.com/bankcgi_dev/ofx_server',
        'bankid' : '121202211',
        },
    'edward_jones' : {
        'caps' : [ 'SIGNON', 'INVSTMT'],
        'fiorg' : 'www.edwardjones.com',
        'url' : 'https://ofx.edwardjones.com',
        }
    }
'''

class OFXClient:
    '''Encapsulate an ofx client, config is a dict containing configuration'''
    def __init__(self, institution, user, password):
        config = gencfg(institution)
        self.password = password
        self.user = user
        self.config = config
        self.cookie = 3
        config['user'] = user
        config['password'] = password
        if not config.has_key('appid'):
            # i've had to fake Quicken to actually get my unwilling test server to talk to me
            config['appid'] = 'QWIN'
            config['appver'] = '1200'

    def _cookie(self):
        self.cookie += 1
        return str(self.cookie)

    '''Generate signon message'''
    def _signOn(self):
        config = self.config
        fidata = [ field('ORG',config['fiorg']) ]
        if config.has_key('fid'):
            fidata += [ field('FID',config['fid']) ]
        return tag('SIGNONMSGSRQV1',
                    tag('SONRQ',
                         field('DTCLIENT',_date()),
                         field('USERID',config['user']),
                         field('USERPASS',config['password']),
                         field('LANGUAGE','ENG'),
                         tag('FI', *fidata),
                         field('APPID',config['appid']),
                         field('APPVER',config['appver']),
                         ))

    def _acctreq(self, dtstart):
        req = tag('ACCTINFORQ',field('DTACCTUP',dtstart))
        return self._message('SIGNUP','ACCTINFO',req)

#    # this is from _ccreq below and reading page 176 of the latest OFX doc.
#    def _bareq(self, bankname, acctid, dtstart, accttype):
#        config=self.config
#        req = tag('STMTRQ',
#            tag('BANKACCTFROM',
#                field('BANKID',sites [str(bankname)] ['bankid']),
#                    field('ACCTID',acctid),
#                field('ACCTTYPE',accttype)),
#            tag('INCTRAN',
#                field('DTSTART',dtstart),
#                field('INCLUDE','Y')))
#        return self._message('BANK','STMT',req)

    def _ccreq(self, acctid, dtstart):
        req = tag('CCSTMTRQ',
            tag('CCACCTFROM',field('ACCTID',acctid)),
            tag('INCTRAN',
            field('DTSTART',dtstart),
            field('INCLUDE','Y')))
        return self._message('CREDITCARD','CCSTMT',req)

    def _invstreq(self, brokerid, acctid, dtstart):
        dtnow = time.strftime('%Y%m%d%H%M%S',time.localtime())
        req = tag('INVSTMTRQ',
                   tag('INVACCTFROM',
                      field('BROKERID', brokerid),
                      field('ACCTID',acctid)),
                   tag('INCTRAN',
                        field('DTSTART',dtstart),
                        field('INCLUDE','Y')),
                   field('INCOO','Y'),
                   tag('INCPOS',
                        field('DTASOF', dtnow),
                        field('INCLUDE','Y')),
                   field('INCBAL','Y'))
        return self._message('INVSTMT','INVSTMT',req)

    def _message(self,msgType,trnType,request):
        return tag(msgType+'MSGSRQV1',
                    tag(trnType+'TRNRQ',
                         field('TRNUID',_genuuid()),
                         field('CLTCOOKIE',self._cookie()),
                         request))

    def _header(self):
        return join('\r\n',[ 'OFXHEADER:100',
                             'DATA:OFXSGML',
                             'VERSION:102',
                             'SECURITY:NONE',
                             'ENCODING:USASCII',
                             'CHARSET:1252',
                             'COMPRESSION:NONE',
                             'OLDFILEUID:NONE',
                             'NEWFILEUID:'+_genuuid(),
                             ''])

#    def baQuery(self, acctid, dtstart, accttype):
#        '''Bank account statement request'''
#        return join('\r\n',[self._header(),
#                            tag('OFX',
#                                self._signOn(),
#                                self._bareq(acctid, dtstart, accttype))])

    def _ccQuery(self, acctid, dtstart):
        '''CC Statement request'''
        return join('\r\n',[self._header(),
                          tag('OFX',
                               self._signOn(),
                               self._ccreq(acctid, dtstart))])

    def _acctQuery(self,dtstart):
        return join('\r\n',[self._header(),
                          tag('OFX',
                               self._signOn(),
                               self._acctreq(dtstart))])

    def _invstQuery(self, brokerid, acctid, dtstart):
        return join('\r\n',[self._header(),
                          tag('OFX',
                               self._signOn(),
                               self._invstreq(brokerid, acctid,dtstart))])

    ''' Returns the raw text response
    '''
    def _rawquery(self, qtype, dtstart):
        xml = ''
        if qtype == 'account':
            xml = self._acctQuery(dtstart)
#        elif qtype == 'creditcard':
#            xml = self._ccQuery(dtstart)
#        elif qtype == 'investment':
#            xml = self._invstQuery(dtstart)

        headers = {'Content-Type'   : 'application/x-ofx',
                   'Content-Length' : str(len(xml)),
                   'Accept': '*/*, application/x-ofx'}
        r = requests.post(self.config['url'], data=str(xml), headers=headers)
        return str(r.text)

    ''' Parses the returned response by splitting out the OFX header from
    the response, leaving only XML
    '''
    def _parseresponse(self, response):
        return response[response.find('<'):]

    def query(self, qtype, dtstart):
        response = self._rawquery(qtype,dtstart)
        response = self._parseresponse(response)
        return response
'''
    def doQuery(self,query,name):
        # N.B. urllib doesn't honor user Content-type, use urllib2
        request = urllib2.Request(self.config['url'],
                                  query,
                                  { 'Content-type': 'application/x-ofx',
                                    'Accept': '*/*, application/x-ofx'
                                  })
        if 1:
            f = urllib2.urlopen(request)
            response = f.read()
            f.close()

            f = file(name,'w')
            f.write(response)
            f.close()
        else:
                print request
                print self.config['url'], query
'''
            # ...


