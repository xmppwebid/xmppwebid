#!/usr/bin/python
# vim: set expandtab tabstop=4 shiftwidth=4:
# -*- coding: utf-8 -*-

# create_ca <http://xmppwebid.github.com/>
# Create a X509 CA certificate
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
    create_ca
    ~~~~~~~~~~~~~~~

    Create a X509 CA certificate.

    Usage: execute ./create_ca -h

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

__app__ = "create_ca"
__author__ = "Julia Anaya"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 Julia Anaya"
__date__ = "2011/03/01"
__license__ = " GNU GPL version 3 or any later version (details at http://www.gnu.org)"
__credits__ = ""

from xmppwebid import gen_cacert_pemfile
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
  -k, --key-path    CA private key path
  -s, --certificate-serial-path certificate serial number path
  -y  --years                   certificate years
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

    Options:
      -h, --help                    Print this usage message.
      -d, --debug
      -p, --certificate-path        CA certificate path
      -k, --key-path    CA private key path
      -y  --years                   certificate years
      -s, --certificate-serial-path certificate serial number path
      -n, --commmonname             certificate commonName
      -c, --country                 certificate countryName
      -o, --organization            certificate organizationName
      -u, --organizationalunit      certificate organizationalUnitNam
      -e, --email                   certificate emailAddress
    """
    
    serial_path='/tmp/xmppwebid_cert_serial.txt'
    years = 1
    CN = "CA Certificate"
    C = "CR"
    O="xmppwebid community"
    OU="xmppwebid CA cert"
    Email="ca:xmppwebid.github.com"
    cacert_path='/tmp/xmppwebid_cacert.pem'
    cakey_path='/tmp/xmppwebid_cakey.key'
    
    short_opts = "hdp:k:s:y:n:c:o:u:e:"
    long_opts = ["help","debug", "certificate-path=","key-path=", 
      "certificate-serial-path=", "years=", 
      "commonname=", "country=", "organization=",
      "organizationalunit=", "email="]
      
    try:                                
        opts, args = getopt.getopt(argv, short_opts, long_opts)
    except getopt.GetoptError:
        print "The CA certificate will be created with default values"
#        _usage()
#        sys.exit(0)


    for opt, arg in opts:
        if opt in ("-h", "--help"):     
            _usage()                 
            sys.exit(0)
        elif opt in ("-p","--certificate-path"):
            cacert_path = arg
        elif opt in ("-k","--key-path"):
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
        elif opt in ("-s","--certificate-serial-path"):
            serial_path = arg
        elif opt in ("-y","--years"):
            years = arg

    gen_cacert_pemfile(CN, C, O, OU, Email, cacert_path, cakey_path,
                       serial_path, years)
    
if __name__ == "__main__":
    main(sys.argv[1:])
