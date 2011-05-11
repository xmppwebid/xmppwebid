#!/usr/bin/python
# vim: set expandtab tabstop=4 shiftwidth=4:
# -*- coding: utf-8 -*-

# xmpp_foaf_cert <http://xmppwebid.github.com/>
# Python functions for generate a X509 client certificate for XMPP or HTTP
# WebID authentication (including WebId and XMPP id at SubjectAltName).
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
xmpp_foaf_cert

Python functions for generate a X509 client certificate for XMPP or HTTP
 WebID authentication (including WebId and XMPP id at SubjectAltName).

Usage: execute ./xmpp_foaf_cert -h

@author:       julia
@organization: xmppwebid community
@copyright:    author 
@license:      GNU GPL version 3 or any later version 
                (details at http://www.gnu.org)
@contact:      julia dot anaya at gmail dot com
@dependencies: python (>= version 2.4.5)
@change log:
@TODO: 
"""

__app__ = "xmpp_foaf_cert"
__author__ = "julia"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 julia"
__date__ = "2011/03/01"
__license__ = " GNU GPL version 3 or any later version (details at http://www.gnu.org)"
__credits__ = ""

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


import os, time, base64, sys
from M2Crypto import X509, EVP, RSA, Rand, ASN1, m2, util, BIO
import OpenSSL

ID_ON_XMPPADDR_OID = "1.3.6.1.5.5.7.8.5"

DEBUG = True

# Example default values
CA_CN = "CA Certificate"
CA_C = "CR"
CA_O="Rhizomatik Labs"
CA_OU="Mycelia project"
CA_Email="ca@xmppwebid.github.com"
#ST LONDON
#L Wimbledom
# other extensions for cert
"""
            X509v3 Basic Constraints: 
                CA:FALSE
            Netscape Comment: 
                OpenSSL Generated Certificate
            X509v3 Subject Key Identifier: 
                2A:69:21:5C:D6:19:05:D6:AC:33:89:79:89:5E:07:24:9E:9C:C4:13
            X509v3 Authority Key Identifier: 
                keyid:42:D9:0E:FB:7A:B4:D4:EF:BE:5F:4B:87:7E:BE:D3:AD:4C:64:C3:33
                DirName:/C=GB/ST=LONDON/L=Wimbledon/O=FOAF.ME/CN=FOAF.ME/emailAddress=ca@foaf.me
                serial:B8:8B:38:D3:8A:D1:75:E2
"""
# other extensions for ca
"""
            X509v3 Subject Key Identifier: 
                A4:B4:A9:B8:82:BC:FB:58:76:CA:1D:9E:F1:9E:1B:C3:F7:D4:F0:D5
            X509v3 Authority Key Identifier: 
                keyid:A4:B4:A9:B8:82:BC:FB:58:76:CA:1D:9E:F1:9E:1B:C3:F7:D4:F0:D5
                DirName:/CN=Rhizomatik labs TestCA/C=CR/ST=Croatan/L=Here/O=xmppwebid.github.com/emailAddress=info@xmppwebid.github.com
                serial:83:A5:0B:01:E9:2C:37:9B
"""

def mkkeypair(bits):
    """
    Create RSA key pair
    
    @param bits: key bits length
    @type bits: int
    @return: private key 
    @rtype: EVP.PKey
    """
    pk = EVP.PKey()
    rsa = RSA.gen_key(bits, 65537)
    pk.assign_rsa(rsa)
    print "Generated private RSA key"
    # Print the new private key as a PEM-encoded (but unencrypted) string
    if DEBUG: print rsa.as_pem(cipher=None)
    return pk

def mkreq_ca(bits=1024, CN=None, C=None, O=None, OU=None, Email=None):
    """
    Create an x509 CA request
    
    @param bits: (optional) key bits length
    @type bits: int
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
    @return:  x509 request, private key
    @rtype: tuple (X509.Request, EVP.PKey)
    """
    if DEBUG:
        print "CN: "+CN
        print "C: "+C
        print "O: "+O
        print "OU: "+OU
        print "Email: "+Email

    # create key pair (private only?)
    pk = mkkeypair(bits)

    # create x509 request
    x = X509.Request()

    # set public key
    x.set_pubkey(pk)

    x509_name = x.get_subject()
    # optional
#    # Create a new X509_Name object for our new certificate
#    x509_name=X509.X509_Name()
#    # Set the new cert subject

#    x.set_subject_name(x509_name.x509_name)
    # set Subject commonName

#    x509_name.CN = "CA Certificate Request"
#    x509_name.C = "CR"
#    x509_name.O="Rhizomatik Labs"
#    x509_name.OU="Mycelia project"
#    x509_name.Email="ca@xmppwebid.github.com"

    if not CN: CN = CA_CN
    if not C: C = CA_C
    if not O: O = CA_O
    if not OU: OU = CA_OU
    if not Email: Email = CA_Email

    x509_name.CN = CN
    x509_name.C = C
    x509_name.O = O
    x509_name.OU = OU
    x509_name.Email = Email

    # sign the x509 certificate request with private key
    x.sign(pk,'sha1')
    
    print "Generated new CA req"
    if DEBUG: print  x.as_pem()

    return x, pk


def mkreq_client(id_xmpp, webid, bits=1024):
#        ,C=None, O=None, OU=None, Email=None):
    """mkkeypair(bits)
    Create an x509 request
    
    @param bits: key bits length
    @param id_xmpp: xmpp id
    @param webid: FOAF WebId
    @type bits: int
    @type id_xmpp: string
    @type webid: string
    @param C: certificate countryName
    @param O: certificate organizationName
    @param OU: certificate organizationalUnitName
    @param Email: certificate emailAddress
    @type C: string
    @type O: string
    @type OU: string
    @type Email: string
    @return:  x509 request, private key
    @rtype: tuple (X509.Request, EVP.PKey)
    """

    # create key pair (private only?)
    pk = mkkeypair(bits)

    # create x509 request
    x = X509.Request()

    # set public key
    x.set_pubkey(pk)

    x509_name = x.get_subject()

    # set Subject commonName
    x509_name.CN = webid + "/"+ ID_ON_XMPPADDR_OID + "=" + id_xmpp
#    name.CN = webid

    # if the req is going to be signed by a ca
    # there is not need to add CN because the ca cert is going to overwrite it
    # optional
#    # Create a new X509_Name object for our new certificate
#    x509_name=X509.X509_Name()

#    x509_name.C = "CR"
#    x509_name.O="Rhizomatik Labs"
#    x509_name.OU="Mycelia project"
#    x509_name.Email="ca@xmppwebid.github.com"

#    if not C: x509_name.C = CA_C
#    if not O: x509_name.O = CA_O
#    if not OU: x509_name.OU = CA_OU
#    if not Email:x509_name. Email = CA_Email

#    # Set the new cert subject
#    x.set_subject_name(x509_name.x509_name)

    # set subjectAltName extension
    ext1 = X509.new_extension('subjectAltName', 'URI:%s, otherName:%s;UTF8:%s' %(webid, ID_ON_XMPPADDR_OID, id_xmpp))
#    ext1 = X509.new_extension('subjectAltName', 'URI:%s' %webid)
    extstack = X509.X509_Extension_Stack()
    extstack.push(ext1)
    x.add_extensions(extstack)

    # sign the x509 certificate request with private? key
    x.sign(pk,'sha1')
    print "Generated new client req"
    if DEBUG: print x.as_pem()

    return x, pk

def set_valtime(cert):
    """
    Set certificate valid time
    
    @param cert: certificate
    @type cert: X509
    """

#    t = long(time.time()) + time.timezone
    t = int(time.time())
    now = ASN1.ASN1_UTCTIME()
    now.set_time(t)
    print now.get_datetime()
    nowPlusYear = ASN1.ASN1_UTCTIME()
    nowPlusYear.set_time(t + 60 * 60 * 24 * 365)
    # later.set_time(int(time.time()+3600*24*7))
#    return now, nowPlusYear
    cert.set_not_before(now)
    if DEBUG: print cert.get_not_before()
    cert.set_not_after(nowPlusYear)
    if DEBUG: print cert.get_not_after()

def get_serial_from_file(serial_path='/tmp/xmpp_foaf_cert_serial.txt'):
    """
    Get serial number
    
    @param serial_path: serial file path
    @type serial_path: string
    @return: serial number
    @rtype: int
    """
    try:
        serial_file = open(serial_path, "r")
        data = serial_file.read()
        serial_file.close()
        if data: number = int(data)
        number += 1
    except:
        number = 1
    serial_file = open(serial_path, "w")
    serial_file.write(str(number))
    serial_file.close()
    return number

def set_serial(cert, serial_path='/tmp/xmpp_foaf_cert_serial.txt'):
    """
    Set certificate serial number
    
    @param cert: certificate
    @type cert: X509
    @param serial_path: serial file path
    @type serial_path: string
    """
    serial_number = get_serial_from_file(serial_path)
    serial=m2.asn1_integer_new()
    m2.asn1_integer_set(serial,serial_number)
    m2.x509_set_serial_number(cert.x509,serial)
#    return cert

def mkcert_defaults(req, serial_path='/tmp/xmpp_foaf_cert_serial.txt'):
    """
    Create an x509 certificate from x509 certificate request with default values
    
    @param req: x509 certificate request 
    @type cert: X509.Request
    @param serial_path: serial file path
    @type serial_path: string
    @return: x509 certificate
    @rtype: X509.X509
    """

    # create x509 certificate
    cert = X509.X509()
    # get public key from request
    pkey = req.get_pubkey()
    # set public key
    cert.set_pubkey(pkey) # pk if not req create

    # get subject from request
    x509_name = req.get_subject()
#    # Set the new cert subject
    cert.set_subject(x509_name) # the same as if a req subject was created

    # optional
#    cert.set_issuer_name(x509_name.x509_name)
    cert.set_issuer(x509_name)

    # set version
#    cert.set_version(3)
    #@TODO: check that changing jabberd version here can remain 3
    cert.set_version(2)

    #@TODO: set a real serial number
#    cert.set_serial_number(1)
    set_serial(cert)

    # Set Cert validity time
#    now, nowPlusYear = mktime()
#    cert.set_not_before(now)pkcs
#    cert.set_not_after(nowPlusYear)
    set_valtime(cert)

    return cert

def mkcert_selfsigned(id_xmpp, webid):
    """
    Create an x509 self-signed certificate
    
    @param id_xmpp: xmpp id
    @param webid: FOAF WebId
    @type id_xmpp: string
    @type webid: string
    @return:  x509 self-signed certificate, private key
    @rtype: tuple (X509.X509, EVP.PKey)
    """
    req, pk = mkreq_client(id_xmpp, webid)
    cert = mkcert_defaults(req)

    # the cert subject is the same as req subject
    # the issuer is going to be the same, ?

    # set subjectAltName extension
#    ext = X509.new_extension('subjectAltName', 'DNS:foobar.example.com')
    ext = X509.new_extension('subjectAltName', 'URI:%s, otherName:%s;UTF8:%s' %(webid, ID_ON_XMPPADDR_OID, id_xmpp))
#    ext = X509.new_extension('subjectAltName', 'URI:%s' %webid)
    ext.set_critical(0)
    cert.add_ext(ext)

    # sign the x509 certificate with private? key generated in the request
    cert.sign(pk, 'sha1')

    # Print the new certificate as a PEM-encoded string
    print "Generated new self-signed client certificate"
    if DEBUG: print cert.as_pem()

    return cert, pk


def mkcert_casigned(id_xmpp, webid, req, cacert, capk,
        serial_path="/tmp/xmpp_foaf_cert_serial.txt"):
    """
    Create an x509 CA signed certificate
    
    @param id_xmpp: xmpp id
    @param webid: FOAF WebId
    @param cacert: CA certificate
    @param capk: CA private key
    @param seria_path: serial path
    @type id_xmpp: string
    @type webid: string
    @type cacert: X509.X509
    @type capk: EVP.PKey
    @type serial_path: string
    @return:  x509 CA signed certificate
    @rtype: X509.X509
    """

    # the cert public key is the req public key
    cert = mkcert_defaults(req, serial_path)

    # if certificate is going to be signed by a CA

    # this is not optional
    # set the certificate Issuer name as the CA subject name
#    issuer = X509.X509_Name()
#    issuer.C  = "CR"
#    issuer.CN = "Rhizomatik Labs"
#    cert.set_issuer(issuer)
    #cert.set_issuer_name(cacert.get_subject().x509_name)
#    cert.set_issuer_name(x509_name.x509_name)
    cert.set_issuer(cacert.get_subject())

    # set subjectAltName extension
#    ext = X509.new_extension('subjectAltName', 'DNS:foobar.example.com')
    ext = X509.new_extension('subjectAltName', 'URI:%s, otherName:%s;UTF8:%s' %(webid, ID_ON_XMPPADDR_OID, id_xmpp))
#    ext = X509.new_extension('subjectAltName', 'URI:%s' %webid)
    ext.set_critical(0)
    cert.add_ext(ext)

    # sign the x509 certificate with private? key generated in the request
    cert.sign(capk, 'sha1')

    # verify
    print "Client certificate verfication with CA certificate public key"
    print m2.x509_verify(cert.x509, m2.x509_get_pubkey(cacert.x509))

    # Print the new certificate as a PEM-encoded string
    print "Generated new client certificate signed with CA"
    if DEBUG: print cert.as_pem()
    return cert

def mkcacert(CN=None, C=None, O=None, OU=None, Email=None):
    """
    Create an x509 CA certificate
    
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
    @return:  x509 CA certificate, CA private key
    @rtype: tuple (X509.X509, EVP.PKey)
    """
    req, pk = mkreq_ca(CN=CN, C=C, O=O, OU=OU, Email=Email)
    cert = mkcert_defaults(req)

    # this is not optional
    # set the CA certificate Subject name
    # is allready assigned in mkcert_defaults
#    name = cert.get_subject()
#    name.C = "CR"
#    name.CN = "Rhizomatik Labs"

    # this is not optional
    # set the CA certificate Issuer name
    # is allready assigned in mkcert_defaults
#    issuer = X509.X509_Name()
#    issuer.C = "CR"
#    issuer.CN = "Rhizomatik Labs"
#    cert.set_issuer(issuer)

    # set basicConstraints extension
    ext = X509.new_extension('basicConstraints', 'CA:TRUE')
    cert.add_ext(ext)

    # sign the x509 CA certificate with private? key generated in the request
    cert.sign(pk, 'sha1')

    print "Generated new CA certificate"
    # Print the new certificate as a PEM-encoded string
    if DEBUG: print cert.as_pem()

    return cert, pk

def mkcacert_save(cacert_path='/tmp/xmpp_foaf_cacert.pem', 
        cakey_path='/tmp/xmpp_foaf_cakey.key', 
        CN=None, C=None, O=None, OU=None, Email=None):
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
    @return:  x509 CA certificate, CA private key
    @rtype: tuple (X509.X509, EVP.PKey)
    """
    # create ca cert
    cacert, capk = mkcacert(CN, C, O, OU, Email)
    # save key without ask for password
    capk.save_key(cakey_path, None)
    cacert.save_pem(cacert_path)
    return cacert, capk

def get_cacert_cakey_from_file(cacert_path='/tmp/xmpp_foaf_cacert.pem', 
        cakey_path='/tmp/xmpp_foaf_cakey.key'):
    """
    Get an x509 CA certificate and CA private key from a PEM CA certificate file
    
    @param cacert_path: CA certificate path
    @param cakey_path: CA private key path
    @type cacert_path: string
    @type cakey_path: string
    @return:  x509 CA certificate, CA private key
    @rtype: tuple (X509.X509, EVP.PKey)
    """
    # with ca cert from file
    # Load the CA certificate and private key
    cacert=X509.load_cert(cacert_path)
    ca_priv_rsa=RSA.load_key(cakey_path)
    capk=EVP.PKey()
    capk.assign_rsa(ca_priv_rsa)
    return cacert, capk

def get_modulus_exponent_from_cert_file(cert_path='/tmp/xmpp_foaf_cert.pem'):
    """
    Get the modulus and exponent of RSA Public Key from a PEM Certificate file
    m2.rsa_get_e(rsa.rsa) return something like '\x00\x00\x00\x03\x01\x00\x01'
    so to get the decimal value (65537), two crufty methods
    
    @param cert_path: certificate path
    @type cert_path: string
    @return: tuple(modulus, exponent)
    @rtype: tuple (hex, int)
    @TODO: replace the exponent method with something cleaner
    """
    cert=X509.load_cert(cert_path)
    pubkey = cert.get_pubkey()
    modulus = pubkey.get_modulus()
    
    pk_rsa = pubkey.get_rsa()
    e  = m2.rsa_get_e(rsa.rsa)
#    exponent = int(eval(repr(e[-3:]).replace('\\x', '')),16)
    exponent = int(''.join(["%2.2d" % ord(x) for x in e[-3:]]),16)
    
    return modulus, exponent

def get_modulus_exponent_from_cert_pk_file(cert_path='/tmp/xmpp_foaf_cert.pem', 
        key_path='/tmp/xmpp_foaf_key.key'):
    """
    Get the modulus and exponent of RSA Public Key from a PEM Certificate and
    private key files
    m2.rsa_get_e(rsa.rsa) return something like '\x00\x00\x00\x03\x01\x00\x01'
    so to get the decimal value (65537), two crufty methods
    
    @param cert_path: certificate path
    @type cert_path: string
    @param key_path: private key path
    @type key_path: string
    @return: tuple(modulus, exponent)
    @rtype: tuple (hex, int)
    @TODO: replace the exponent method with something cleaner
    """
    cert=X509.load_cert(cert_path)
    pubkey = cert.get_pubkey()
    modulus = pubkey.get_modulus()
    
    pk_rsa = RSA.load_key(key_path)
    e  = m2.rsa_get_e(pk_rsa.rsa)
#    exponent = int(eval(repr(e[-3:]).replace('\\x', '')),16)
    exponent = int(''.join(["%2.2d" % ord(x) for x in e[-3:]]),16)
    
    return modulus, exponent

def mkcert_selfsigned_save(cert_path='/tmp/xmpp_foaf_cert.pem', 
        key_path='/tmp/xmpp_foaf_key.key'):
    """
    Create an x509 self-signed certificate and save it as PEM file
    
    @param cert_path: certificate path
    @param key_path: private key path
    @type cert_path: string
    @type key_path: string
    @return:  x509 certificate, private key
    @rtype: tuple (X509.X509, EVP.PKey)
    """
    # create self-signed certificate
    cert, pk = mkcert_selfsigned(id_xmpp, webid)
    # save key without ask for password
    pk.save_key(key_path, None)
    cert.save_pem(cert_path)
    # to check
    #R  = req.as_der()
    #from pyasn1.codec.der import decoder as asn1
    # a = asn1.decode(R)
    return cert, pk

def mkcert_casigned_from_file(id_xmpp, webid, 
        cacert_path='/tmp/xmpp_foaf_cacert.pem', 
        cakey_path='/tmp/xmpp_foaf_cakey.key',
        serial_path='/tmp/xmpp_foaf_cert_serial.txt'):
    """
    Create an x509 CA signed certificate from CA certificate and private key 
    PEM files
    
    @param id_xmpp: xmpp id
    @param webid: FOAF WebId
    @type id_xmpp: string
    @type webid: string
    @param cacert_path: CA certificate path
    @param cakey_path: CA private key path
    @param serial_path: certificate serial path
    @type cacert_path: string
    @type cakey_path: string
    @type serial_path: string
    @return:  x509  certificate, private key
    @rtype: tuple (X509.X509, EVP.PKey)
    """
    # with recently generated ca cert
    cacert, capk = get_cacert_cakey_from_file(cacert_path, cakey_path)
    req, pk = mkreq_client(id_xmpp, webid)
    cert = mkcert_casigned(id_xmpp, webid, req, cacert, capk, serial_path)
    return cert, pk

def mkcert_casigned_from_file_save(id_xmpp, webid, 
        cacert_path='/tmp/xmpp_foaf_cacert.pem', 
        cakey_path='/tmp/xmpp_foaf_cakey.key', 
        cert_path='/tmp/xmpp_foaf_cert.pem', 
        key_path='/tmp/xmpp_foaf_key.key',
        serial_path='/tmp/xmpp_foaf_cert_serial.txt'):
    """
    Create an x509 CA signed certificate from CA certificate and private key 
    files and save the CA signed certificate and private key in files as PEM
    
    @param id_xmpp: xmpp id
    @param webid: FOAF WebId
    @type id_xmpp: string
    @type webid: string
    @param cacert_path: CA certificate path
    @param cakey_path: CA private key path
    @type cacert_path: string
    @type cakey_path: string
    @param cert_path: certificate path
    @param key_path: private key path
    @param serial_path: certificate serial path
    @type cert_path: string
    @type key_path: string
    @type serial_path: string
    @return:  x509  certificate, private key
    @rtype: tuple (X509.X509, EVP.PKey)
    """
    cacert, capk = get_cacert_cakey_from_file(cacert_path, cakey_path)
    req, pk = mkreq_client(id_xmpp, webid)
    cert = mkcert_casigned(id_xmpp, webid, req, cacert, capk, serial_path)
    cert.save_pem(cert_path)
    print "saved cert: %s" % cert_path
    pk.save_key(key_path, None)
    return cert, pk

def pkcs12cert(cert_path='/tmp/xmpp_foaf_cert.pem', 
        key_path='/tmp/xmpp_foaf_key.key', 
        p12cert_path='/tmp/xmpp_foaf_cert.p12'):
    """
    Create a PKCS12 certificate and save it from x509 certificate and private 
    key files as PEM
    
    @param cert_path: certificate path
    @param key_path: private key path
    @param p12cert_path: private key path
    @type cert_path: string
    @type key_path: string
    @type p12cert_path: string
    @return: PKCS12 certificate path
    @rtype: string
    @TODO: create pkcs12 m2crypto function 
            (http://osdir.com/ml/python.cryptography/2004-05/msg00001.html)
    @TODO: create pkcs12 with password interactively
    """
    pk = OpenSSL.crypto.load_privatekey(OpenSSL.SSL.FILETYPE_PEM, open(key_path).read())
    cert = OpenSSL.crypto.load_certificate(OpenSSL.SSL.FILETYPE_PEM, open(cert_path).read())
    p12 = OpenSSL.crypto.PKCS12()
    p12.set_privatekey(pk)
    p12.set_certificate(cert)
    # @TODO: without key
    p12cert = open(p12cert_path,"w")
    p12cert.write(p12.export())
    p12cert.close()
    return p12cert_path


def cert_from_pkcs12(cert_path='/tmp/xmpp_foaf_cert.pem', 
        key_path='/tmp/xmpp_foaf_key.key', 
        p12cert_path='/tmp/xmpp_foaf_cert.p12'):
    """
    Get X509 certificate and private key from PKCS12 file and save them as PEM
    key files as PEM
    
    @param cert_path: certificate path
    @param key_path: private key path
    @param p12cert_path: private key path
    @type cert_path: string
    @type key_path: string
    @type p12cert_path: string
    @TODO: get pkcs12 with password interactively
    """
    p12 = OpenSSL.crypto.load_pkcs12(open(p12cert_path).read())
    cert = p12.get_certificate()
    pk = p12.get_privatekey()
    certdump = OpenSSL.crypto.dump_certificate(OpenSSL.SSL.FILETYPE_PEM, cert)
    cert_file = open(cert_path, "w")
    cert_file.write(certdump)
    cert_file.close()
    pkeydump = OpenSSL.crypto.dump_privatekey(OpenSSL.SSL.FILETYPE_PEM, pk)
    pkey_file = open(key_path, "w")
    pkey_file.write(pkeydump)
    pkey.close()
    pkey_file.close()

def pemcert(cert_path='/tmp/xmpp_foaf_cert.pem', 
        key_path='/tmp/xmpp_foaf_key.key',
        certkey_path='/tmp/xmpp_foaf_cert_key.pem'):
    """
    Create a PEM file with X509 certificate and private key from PEM files
    
    @param cert_path: certificate path
    @param key_path: private key path
    @param certkey_path: private key path
    @type cert_path: string
    @type key_path: string
    @type certkey_path: string
    @return: PEM file with X509 certificate and private key path
    @rtype: string
    """
    cert = open(cert_path)
    cert_data = cert.read()
    cert.close()
    key = open(key_path)
    cert_data += key.read()
    key.close()
    certkey = open(certkey_path, "w")
    certkey.write(cert_data)
    certkey.close()
    return certkey_path

def main(argv):
    id_xmpp = "julia@xmpp.xmppwebid.github.com"
    webid = "http://xmppwebid.github.com/xmppwebid/julia#me"
    
    mkcacert_save()
    mkcert_casigned_from_file_save(id_xmpp, webid)
    p12cert_path = pkcs12cert()
#    p12cert_path = pkcs12cert_from_file_save()
#    cert, capk = mkcert_casigned_from_file(id_xmpp, webid)
#    p12cert_path = pkcs12cert(cert, capk)

if __name__ == "__main__":
    main(sys.argv[1:])
