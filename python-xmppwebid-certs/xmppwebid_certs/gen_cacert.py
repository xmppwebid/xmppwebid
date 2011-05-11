#!/usr/bin/python
# vim: set expandtab tabstop=4 shiftwidth=4:
# -*- coding: utf-8 -*-

# gen_cacert <http://xmppwebid.github.com/>
# Python functions for generate a X509 CA certificate 
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
gen_cacert

Python functions for generate a X509 CA certificate.

Usage: execute ./gen_cacert -h

@author:       julia
@organization: xmppwebid community
@copyright:    author 
@license:      GNU GPL version 3 or any later version 
                (details at http://www.gnu.org)
@contact:      julia dot anaya at gmail dot com
@dependencies: python (>= version 2.5)
@change log:
@TODO: 
 * Get error/warning when some of the main parameters have space and th
at and the nexts get ignored
 * Add paramter for certificate serial path
"""

__app__ = "gen_cacert"
__author__ = "julia"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 julia"
__date__ = "2011/03/01"
__license__ = " GNU GPL version 3 or any later version (details at http://www.gnu.org)"
__credits__ = ""

from xmpp_foaf_cert import *
import sys
import getopt

DEBUG = True

## ----------------------------------------------------------------------
## administrative functions
## ----------------------------------------------------------------------

def _usage():
    print "Usage: %s options" % __app__
    print """
Options:
  -h, --help                    Print this usage message.
  -d, --debug
  -p, --certificate-path        CA certificate path
  -k, --certificate-key-path    CA private key path
  -n, --commmonname             certificate commonName
  -c, --country                 certificate countryName
  -o, --organization            certificate organizationName
  -u, --organizationalunit      certificate organizationalUnitNam
  -e, --email                   certificate emailAddress
"""

def _version():
    """
    Display a formatted version string for the module
    """
    print """%(__app__)s %(__version__)s
%(__copyright__)s
released %(__date__)s

Thanks to:
%(__credits__)s""" % globals()


def main(argv):
    """
    Create an x509 CA certificate and save it as PEM file
    
    @param CN: certificate commonName
    @param C: certificate countryName
    @param O: certificate organizationName
    @param OU: certificate organizationalUnitName
    @param Email: certificate emailAddress
    @type CN: string
    @type C: string
    @type O: string
    @type OU: string
    @type Email: string
    @param cacert_path: CA certificate path
    @param cakey_path: CA private key path
    @type cacert_path: string
    @type cakey_path: string
    """
    short_opts = "hdp:k:n:c:o:u:e:"
    long_opts = ["help","debug", "certificate-path=","certificate-key-path=","commonname=","country=","organization=","organizationalunit=","email="]
    try:                                
        opts, args = getopt.getopt(argv, short_opts, long_opts)
    except getopt.GetoptError:
        print "The CA certificate will be created with default values"
#        _usage()
#        sys.exit(0)

    # Example default values
    CN = "CA Certificate"
    C = "CR"
    O="Rhizomatik Labs"
    OU="Mycelia project"
    Email="ca@xmppwebid.github.com"
    cacert_path='/tmp/xmpp_foaf_cacert.pem'
    cakey_path='/tmp/xmpp_foaf_cakey.key'

    for opt, arg in opts:
        if opt in ("-h", "--help"):     
            _usage()                 
            sys.exit(0)
        elif opt in ("-p","--certificate-path"):
            cacert_path = arg
        elif opt in ("-k","--certificate-key-path"):
            cakey_path = arg
        elif opt in ("-n","--commmonname"):
            CN = arg
        elif opt in ("-c","--country"):
            C = arg
        elif opt in ("-o","--organization"):
            O = arg
        elif opt in ("-u","--organizationalunit"):
            OU = arg
        elif opt in ("-e","--email"):
            Email = arg
    if DEBUG:
        print "CN: "+CN
        print "C: "+C
        print "O: "+O
        print "OU: "+OU
        print "Email: "+Email

    mkcacert_save(cacert_path, cakey_path, CN, C, O, OU, Email)
    
if __name__ == "__main__":
    main(sys.argv[1:])
