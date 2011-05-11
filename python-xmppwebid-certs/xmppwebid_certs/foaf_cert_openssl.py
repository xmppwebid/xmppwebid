#!/usr/bin/python
#!/usr/bin/python
# vim: set expandtab tabstop=4 shiftwidth=4:
# -*- coding: utf-8 -*-

# foaf_cert_openssl <http://xmppwebid.github.com/>
# Python functions for generate a X509 client certificate (with OpenSSL) for 
# WebID authentication (including WebId at SubjectAltName).
#
# Copyright (C) 2009 julia dot anaya at gmail dot com
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
foaf_cert_openssl

Python functions for generate a X509 client certificate (with OpenSSL commands
) for WebID authentication (including WebId at SubjectAltName).
This module is deprecated as xmpp_foaf_cert makes the same with m2crypto and 
pyopenssl libraries and create de certificates valid for XMPP too.

Usage: execute ./foaf_cert_openssl -h

@author:       julia
@organization: xmppwebid community
@copyright:    author 
@license:      GNU GPL version 3 or any later version 
                (details at http://www.gnu.org)
@contact:      julia dot anaya at gmail dot com
@dependencies: python (>= version 2.4.5)
@change log:
@TODO: implement with pyOpenSSL or M2Crypto
"""

__app__ = "foaf_cert_openssl"
__author__ = "julia"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2009 julia"
__date__ = "2009/10/23"
__license__ = " GNU GPL version 3 or any later version (details at http://www.gnu.org)"
__credits__ = ""

import sys
## ----------------------------------------------------------------------
## administrative functions
## ----------------------------------------------------------------------

def _usage():
    print "Usage: %s " % __app__
    print """
Options:
  -h, --help      Print this usage message.
  -d,             debug
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


import tempfile
import sys
import os
from string import Template


def create_openssl(name, webid, openssl_custom_file_path=None, openssl_private_key_file_path=None, openssl_file_path="data/openssl-foaf.cnf"):
    if openssl_file_path:
        openssl_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), openssl_file_path)
    if not  openssl_custom_file_path:
        openssl_custom_file_path = "/tmp/%s_openssl-foaf.cnf" % name
    if not openssl_private_key_file_path:
        openssl_private_key_file_path = "/tmp/%s_privatekey.pem" % name
    print openssl_file_path
    openssl_file = open(openssl_file_path, "r")
    openssl_template_data = openssl_file.read()
    openssl_file.close()
    openssl_data = Template(openssl_template_data)
    openssl_data = openssl_data.substitute(name = name, webid = webid, openssl_private_key_file_path = openssl_private_key_file_path)
    openssl_custom_file = open(openssl_custom_file_path, "w")
    openssl_custom_file.write(openssl_data)
    openssl_custom_file.close()
    print "Generated new openssl config file " + openssl_custom_file_path
    return openssl_custom_file_path, openssl_private_key_file_path

def generate_cert_x509(name, openssl_custom_file_path=None, openssl_cert_file_path=None):
    if not  openssl_custom_file_path:
        openssl_custom_file_path = "/tmp/%s_openssl-foaf.cnf" % name
    if not openssl_cert_file_path:
        openssl_cert_file_path = "/tmp/%s_cert.pem" % name
    command = "openssl req -x509 -nodes -newkey rsa:1024 -config %s -out %s" % (openssl_custom_file_path, openssl_cert_file_path)
    print "Generated new X509 cert wiht command: " + command
    try:
        output = os.system(command)
    except Exception, details:
        print "Something bad ocurred: " +  details
#        print "Error % ocurred trying to execute command %s" % (sys.exc_info()[0],command)
        sys.exit()
    return openssl_cert_file_path

def export_pkcs12(name, openssl_cert_file_path=None, openssl_private_key_file_path=None, openssl_pkcs12_file_path=None):
    if not  openssl_pkcs12_file_path:
        openssl_pkcs12_file_path = "/tmp/%s_cert.p12" % name
    if not openssl_cert_file_path:
        openssl_cert_file_path = "/tmp/%s_cert.pem" % name
    if not openssl_private_key_file_path:
        openssl_private_key_file_path = "/tmp/%s_privatekey.pem" % name
    command = "openssl pkcs12 -export -in %s -inkey %s -out %s" % (openssl_cert_file_path, openssl_private_key_file_path, openssl_pkcs12_file_path)
    print "Generated PKCS#12 format wiht command: " + command
    try:
        output = os.system(command)
    except Exception, details:
        print "Something bad ocurred: " + details
        sys.exit()
    return openssl_pkcs12_file_path


def pkcs12cert_from_file_save(cert_path='/tmp/xmpp_foaf_cert.pem', 
        key_path='/tmp/xmpp_foaf_cakey.key', 
        p12cert_path='/tmp/xmpp_foaf_cert.p12'):
    # Instantiate an SMIME object; set it up; sign the buffer.
    command = "openssl pkcs12 -export -in %s -inkey %s -out %s" % (cert_path, key_path, p12cert_path)
    os.system(command)
    return p12cert_path



def main(argv):
#    tmpSPKACfname, tmpCERTfname, SAN = create_identity_x509(foafLocation="http://bblfish.net/people/henry/card#me", 
#        commonName="Henry Story", pubkey="password")
    name = "henrystory"
    webid = "http://bblfish.net/people/henry/card#me"
#    openssl_file_path = "data/openssl-foaf.cnf"
#    openssl_custom_file_path = "/tmp/%s_openssl-foaf.cnf" % (name)
#    openssl_cert_file_path = "/tmp/%s_cert.pem" % name
#    openssl_private_key_file_path = "/tmp/%s_privatekey.pem" % name
#    openssl_pkcs12_file_path = "/tmp/%s_cert.p12" % name
#    create_openssl(name, webid, openssl_file_path, openssl_custom_file_path)
#    create_openssl(name, webid, openssl_custom_file_path)
    create_openssl(name, webid)
#    generate_cert_x509(openssl_custom_file_path, openssl_cert_file_path)
    generate_cert_x509(name)
#    export_pkcs12(openssl_cert_file_path, openssl_private_key_file_path, openssl_pkcs12_file_path)
    openssl_pkcs12_file_path = export_pkcs12(name)

if __name__ == "__main__":
    main(sys.argv[1:])
