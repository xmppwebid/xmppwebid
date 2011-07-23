#!/usr/bin/python
# vim: set expandtab tabstop=4 shiftwidth=4:
# -*- coding: utf-8 -*-

# create_xmppwebid_selfsigned_cert <http://xmppwebid.github.com/>
# Create a X509 self-signed certificate valid for XMPP or HTTP
# WebID authentication
#
# Copyright (C) 2011 julia dot anaya at gmail dot com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
"""
    create_xmppwebid_selfsigned_cert
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Create a X509 self-signed certificate valid for XMPP or HTTP
    WebID authentication

    Usage: execute ./create_xmppwebid_selfsigned_cert -h

    :author:       Julia Anaya
    :organization: xmppwebid community
    :copyright:    author 
    :license:      GNU GPL version 3 or any later version 
                    (details at http://www.gnu.org)
    :contact:      julia dot anaya at gmail dot com
    :dependencies: python (>= version 2.6)
    :change log:
    :TODO: 
"""

__app__ = "create_xmppwebid_selfsigned_cert"
__author__ = "Julia Anaya"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 Julia Anaya"
__date__ = "2011/03/01"
__license__ = " GNU GPL version 3 or any later version (details at http://www.gnu.org)"
__credits__ = ""

from xmppwebid import gen_xmppwebid_selfsigned_cert_pemfile, \
    pemfile_2_pkcs12file, \
    get_modulus_exponent_from_cert_and_pkey_pemfile

import sys
import getopt


## ----------------------------------------------------------------------
## administrative functions
## ----------------------------------------------------------------------

def _usage():
    print "Usage: %s options" % __app__
    print """
Options:
  -h, --help                    Print this usage message.
  -d, --debug
  -p, --certificate-path        PEM certificate path
  -k, --key-path                PEM private key path
  -q, --certificate-key-path    PEM certificate + key path
  -c, --certificate-pkcs12-path PKCS12 certificate path
  -s, --certificate-serial-path certificate serial number path
  -y  --years                   certificate years
  -w, --webid-uri               WebID URI 
  -x, --xmpp-id                 XMPP id (JID)
"""

def _version():
    """Display a formatted version string for the module
    """
    print """%(__app__)s %(__version__)s
%(__copyright__)s
released %(__date__)s

Thanks to:
%(__credits__)s""" % globals()


def main(argv):
    """Create an x509 XMPPWebID certificate and save it as PEM file
    
    Options:
      -h, --help                    Print this usage message.
      -d, --debug
      -p, --certificate-path        PEM certificate path
      -k, --key-path                PEM private key path
      -q, --certificate-key-path    PEM certificate + key path
      -c, --certificate-pkcs12-path PKCS12 certificate path
      -s, --certificate-serial-path certificate serial number path
      -y  --years                   certificate years
      -w, --webid-uri               WebID URI 
      -x, --xmpp-id                 XMPP id (JID)
    """
    cert_path='/tmp/xmppwebid_cert.pem'    
    key_path='/tmp/xmppwebid_key.key'
    certkey_path='/tmp/xmppwebid_cert_key.pem'
    p12cert_path='/tmp/xmppwebid_cert.p12'
    serial_path='/tmp/xmppwebid_cert_serial.txt'
    years = 1
    id_xmpp = ""
    webid = "http://xmppwebid.github.com/xmppwebid/julia#me"
    
    short_opts = "hdp:k:q:c:s:y:w:x:"
    long_opts = ["help","debug", "certificate-path=","key-path=", 
      "certificate-key-path=", "certificate-pkcs12-path=", 
      "certificate-serial-path=", "years=", "webid-uri=", "xmpp-id="]
    try:                                
        opts, args = getopt.getopt(argv, short_opts, long_opts)
    except getopt.GetoptError:
        print "The certificate will be created with default values"
#        _usage()
#        sys.exit(0)

    for opt, arg in opts:
        if opt in ("-h", "--help"):     
            _usage()                 
            sys.exit(0)
        elif opt in ("-p","--certificate-path"):
            cert_path = arg
        elif opt in ("-k","--key-path"):
            key_path = arg
        elif opt in ("-q","--certificate-key-path"):
            certkey_path = arg
        elif opt in ("-c","--certificate-pkcs12-path"):
            p12cert_path = arg
        elif opt in ("-s","--certificate-serial-path"):
            serial_path = arg
        elif opt in ("-y","--years"):
            years = arg
        elif opt in ("-w","--webid-uri"):
            webid = arg
        elif opt in ("-x","--xmpp-id"):
            id_xmpp = arg

    gen_xmppwebid_selfsigned_cert_pemfile(id_xmpp, webid, cert_path, key_path, 
                                          serial_path, years)
    pemfile_2_pkcs12file(cert_path, key_path, p12cert_path)
    modulus, exponent = get_modulus_exponent_from_cert_and_pkey_pemfile(
                                                        cert_path, key_path)
    fd = open('/tmp/modulus.txt','w')
    fd.write(modulus)
    fd.close()
    fd = open('/tmp/exponent.txt','w')
    fd.write(str(exponent))
    fd.close()
    
    
if __name__ == "__main__":
    main(sys.argv[1:])
