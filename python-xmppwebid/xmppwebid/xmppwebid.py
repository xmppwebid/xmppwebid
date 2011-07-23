#!/usr/bin/python
# vim: set expandtab tabstop=4 shiftwidth=4:
# -*- coding: utf-8 -*-

# xmppwebid_utils <http://xmppwebid.github.com/>
# Python functions to generate a X509 client certificate for XMPP or HTTP
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
    xmppwebid_utils
    ~~~~~~~~~~~~~~~

    Python functions for generate a X509 client certificate for XMPP or HTTP
    WebID authentication (including WebId and XMPP id at SubjectAltName).

    :author:       Julia Anaya
    :organization: xmppwebid community
    :copyright:    author 
    :license:      GNU GPL version 3 or any later version 
                    (details at http://www.gnu.org)
    :contact:      julia dot anaya at gmail dot com
    :dependencies: python (>= version 2.6), m2crypto (>= version 0.20),
                   pyopenssl (>= version 0.12)
    :change log:
    
    .. TODO:: 
"""

__app__ = "xmppwebid_utils"
__author__ = "Julia Anaya"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 Julia Anaya"
__date__ = "2011/03/01"
__license__ = " GNU GPL version 3 or any later version \
(details at http://www.gnu.org)"
__credits__ = ""

## ----------------------------------------------------------------------
## administrative functions
## ----------------------------------------------------------------------

def _version():
    """Display a formatted version string for the module

    """
    print """%(__app__)s %(__version__)s
%(__copyright__)s
released %(__date__)s

Thanks to:
%(__credits__)s""" % globals()


## ----------------------------------------------------------------------
## import and globals
## ----------------------------------------------------------------------

import os, time, base64, sys
from M2Crypto import X509, EVP, RSA, Rand, ASN1, m2, util, BIO
import OpenSSL
import logging

#MBSTRING_FLAG = 0x1000
#MBSTRING_ASC  = MBSTRING_FLAG | 1

ID_ON_XMPPADDR_OID = "1.3.6.1.5.5.7.8.5"

# Terminology:
#C Country
#CA Certificate authority
#CN Common Name
#CSR Certificate signing request
#DER Distinguished Encoding Rules
#O Organization
#OU Organizational Unit

# Default certificate Subject, Issuer
O = 'FOAF+SSL'
OU ='The Community of Self Signers'
CN = "Not a Certification Authority"


__all__ = [
 'get_serial_from_file',
 'set_serial',
 'set_valtime',
 
 'gen_keypair',
 
 'gen_csr',
 'set_csr_subject',
 'set_csr_xmppwebid',
 'sign_csr',
 
 'gen_cert_from_csr',
 'set_cert_xmppwebid',
 'sign_cert',
 
# 'save_pkey_cert_to_pemfile',
 'save_pkey_cert_to_pemfile',
 
 'gen_xmppwebid_selfsigned_cert',
 'gen_xmppwebid_selfsigned_cert_pemfile',
 
 'set_cacert',
 'set_casigned_cert',
 'gen_cacert',
 'gen_cacert_pemfile',
 'gen_xmppwebid_casigned_cert',
 'gen_xmppwebid_casigned_cert_pemfile', 
 
 'pkey_cert_2_pkcs12cert',
 'save_pkcs12cert_to_pkcs12file',
 'pemfile_2_pkcs12file',
 
 'get_pkcs12cert_from_pkcs12file',
 'get_cert_pkey_from_pkcs12cert',
 'pkcs12file_2_pemfile',
 
 'get_cert_from_certpemfile',
 'get_pkey_from_pkeypemfile',
 'certpemfile_pkeypemfile_2_certpemfile',
 
 'get_modulus_exponent_from_cert_and_pkey_pemfile',
 'get_modulus_exponent_from_certpemfile',
 'get_modulus_exponent_from_pkcs12file',
 'get_modulus_exponent_from_FOAF',
 
 'check_csr', 
 'validate_xmppwebid_rsa',
 'verify_CA_cert']

## ----------------------------------------------------------------------
## functions
## ----------------------------------------------------------------------


def get_serial_from_file(serial_path='/tmp/xmppwebid_cert_serial.txt'):
    """Get serial number from file
    
    :param serial_path: serial file path
    :type serial_path: string
    :return: serial number
    :rtype: int

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
    
def set_valtime(cert, years=1):
    """Set certificate valid time
    
    :param cert: certificate
    :type cert: X509.X509
    :param years: number of years the certificate is going to be valid
    :type years: int

    """
    days = years*365
#    t = long(time.time()) + time.timezone
    t = int(time.time())
    now = ASN1.ASN1_UTCTIME()
    now.set_time(t)
    logging.debug(now.get_datetime())
    nowPlusYear = ASN1.ASN1_UTCTIME()
    nowPlusYear.set_time(t + 60 * 60 * 24 * days)
    # later.set_time(int(time.time()+3600*24*7))
#    return now, nowPlusYear
    cert.set_not_before(now)
    logging.debug(cert.get_not_before())
    cert.set_not_after(nowPlusYear)
    logging.debug(cert.get_not_after())

def set_serial(cert, serial_number=0):
    """Set certificate serial number
    
    :param cert: certificate
    :type cert: X509.X509
    :param serial_number: certificate serial number
    :type serial_number: string

    """
    serial=m2.asn1_integer_new()
    m2.asn1_integer_set(serial,serial_number)
    m2.x509_set_serial_number(cert.x509,serial)
#    return cert

def gen_keypair(bits=1024):
    """Create RSA key pair
    Equivalent to: openssl genrsa -des3 -out client.key 1024
    
    :param bits: key bits length
    :type bits: int
    :return: key 
    :rtype: EVP.PKey

    """
    pkey = EVP.PKey()
    rsa = RSA.gen_key(bits, 65537)
    pkey.assign_rsa(rsa)
    print "Generated private RSA key"
    # Print the new key as a PEM-encoded (but unencrypted) string
    logging.debug(rsa.as_pem(cipher=None))
    return pkey

def gen_csr(pkey):
    """Create an x509 CSR (Certificate Signing Request)
    Equivalent to: openssl req -new -key client.key -out client.csr
    
    :param pkey: key 
    :type pkey: EVP.PKey
    :return: x509 request
    :rtype: X509.Request
    
    """

    csr = X509.Request()
    csr.set_pubkey(pkey)
    return csr

def set_csr_xmppwebid(csr, id_xmpp, webid):
    """Set the CSR SubjectAltName and Subject

    :param csr:  x509 request
    :type csr: X509.Request    
    :param id_xmpp: xmpp id
    :param webid: FOAF WebId
    :type id_xmpp: string
    :type webid: string
    :return: x509 request
    :rtype: X509.Request
    
    """  
    # if the req is going to be signed by a ca
    # there is not need to add CN because the ca cert is going to overwrite it
    # optional
    # Create a new X509_Name object for our new certificate
    x509_name = X509.X509_Name()
    x509_name.O = O
    x509_name.OU = OU #+"/UID="+webid
    # set Subject commonName
    x509_name.CN ="(Personal)"#+webid + "/"+ ID_ON_XMPPADDR_OID + "=" + id_xmpp
    
#    x509_name.add_entry_by_txt(field='CN', type=MBSTRING_ASC, 
#        entry='(Personal)'+webid + 
#              '/'+ ID_ON_XMPPADDR_OID + '=' + id_xmpp, len=-1, loc=-1, set=0 ) 
        
    logging.debug("Subject name in CSR: %s" % x509_name)
    print "Subject name in CSR: %s" % x509_name
        
    # Set the subject
    csr.set_subject_name(x509_name)

    # set subjectAltName extension
    ext1 = X509.new_extension('subjectAltName', 
         'URI:%s, otherName:%s;UTF8:%s' % (webid, ID_ON_XMPPADDR_OID, id_xmpp))
    extstack = X509.X509_Extension_Stack()
    extstack.push(ext1)
    csr.add_extensions(extstack)
    return csr

def set_csr_subject(csr, CN=None, C=None, O=None, OU=None, Email=None):
    """Set the CSR Subject data
    
    :param CN: certificate commonName
    :param C: certificate countryName
    :param O: certificate organizationName
    :param OU: certificate organizationalUnitName
    :param Email: certificate emailAddress
    :type CN: string
    :type C: string
    :type O: string
    :type OU: string
    :type Email: string
    :return: x509 request
    :rtype: X509.Request

    """
    x509_name = X509.X509_Name()
    x509_name.CN = CN
    x509_name.C = C
    x509_name.O = O
    x509_name.OU = OU
    x509_name.Email = Email
    csr.set_subject_name(x509_name)
    return csr
    
def sign_csr(pkey, csr):
    """Sign the CSR
    
    :param pkey: key 
    :type pkey: EVP.PKey
    :param csr:  x509 request
    :type csr: X509.Request 
    :return: x509 request, key
    :rtype: X509.Request, EVP.PKey

    """
    csr.sign(pkey,'sha1')
    print "Generated new client CSR"
    logging.debug(csr.as_pem())

    return csr, pkey

def gen_cert_from_csr(csr, serial_number=0, years=1):
    """Create an x509 certificate from CSR with default values
    
    :param csr: x509 certificate request 
    :type csr: X509.Request
    :param serial_number: certificate serial number
    :type serial_number: string
    :param years: number of years the certificate is going to be valid
    :type years: int
    :return: x509 certificate
    :rtype: X509.X509
    
    """

    cert = X509.X509()
    pkey = csr.get_pubkey()
    cert.set_pubkey(pkey)

    # the cert subject is the same as csr subject
    # get subject from request
    x509_name = csr.get_subject()
    cert.set_subject(x509_name) # the same if a csr subject was created

    # set version
    #:TODO: check that changing jabberd version here can remain 3
    cert.set_version(2)

    #:TODO: set a real serial number
    set_serial(cert, serial_number)

    set_valtime(cert, years)

    return cert

def set_cert_xmppwebid(cert, id_xmpp, webid):
    """Set the SubjectAltName, Issuer and Subject
    
    :param cert: x509 certificate
    :type cert: X509.X509
    :param id_xmpp: xmpp id
    :param webid: FOAF WebId
    :type id_xmpp: string
    :type webid: string
    :return: x509 certificate
    :rtype: X509.X509

    """
    # optional
    # the issuer is going to be the same as subject
    x509_name = X509.X509_Name()
    x509_name.O = O
    x509_name.OU = OU
    x509_name.CN = CN
    cert.set_issuer(x509_name)

    # set subjectAltName extension
    ext = X509.new_extension('subjectAltName', 
          'URI:%s, otherName:%s;UTF8:%s' %(webid, ID_ON_XMPPADDR_OID, id_xmpp))
    ext.set_critical(1)
    cert.add_ext(ext)
    return cert

def set_cacert(cert, CN=None, C=None, O=None, OU=None, Email=None):
    """Set the SubjectAltName, Issuer and Subject
    
    :param CN: certificate commonName
    :param C: certificate countryName
    :param O: certificate organizationName
    :param OU: certificate organizationalUnitName
    :param Email: certificate emailAddress
    :type CN: string
    :type C: string
    :type O: string
    :type OU: string
    :type Email: string
    :param cert: x509 certificate
    :type cert: X509.X509
    :return: x509 certificate
    :rtype: X509.X509
    
    """
    x509_name = X509.X509_Name()
    x509_name.O = O
    x509_name.OU = OU
    x509_name.CN = CN
    x509_name.Email = Email
    cert.set_issuer(x509_name)
    
#    ext = X509.new_extension('subjectAltName', 'DNS:foobar.example.com')
#    ext.set_critical(0)# Defaults to non-critical, but we can also set it
#    cert.add_ext(ext)

    return cert

def set_casigned_cert(id_xmpp, webid, cacert, cert):
    """
    Set the CA contraint to true
    
    :param cert: x509 certificate
    :type cert: X509.X509
    :return: x509 certificate
    :rtype: X509.X509
    
    """
    # the subject is the CA subject
#    x509_name = cacert.get_subject()
#    print dir(x509_name)
#    cert.set_subject_name(x509_name.x509_name) 
#    cert.set_issuer(x509_name)
    cert.set_issuer(cacert.get_subject())
    
    ext = X509.new_extension('subjectAltName', 
          'URI:%s, otherName:%s;UTF8:%s' %(webid, ID_ON_XMPPADDR_OID, id_xmpp))
    ext.set_critical(1)
    cert.add_ext(ext)   
    ext = X509.new_extension('basicConstraints', 'CA:TRUE')
    cert.add_ext(ext)
    return cert
    
def sign_cert(pkey, cert):
    """Sign the cert
    
    :param pkey: key 
    :type pkey: EVP.PKey
    :param cert:  x509 certificate
    :type cert: X509.X509
    :return: x509 certificate, key
    :rtype: X509.X509, EVP.PKey

    """
    cert.sign(pkey, 'sha1')
    return cert, pkey

def gen_xmppwebid_selfsigned_cert(id_xmpp, webid, serial_number=0, years=1):
    """Create an x509 self-signed certificate
    
    Equivalent to: openssl x509 -req -days 365 -in client.csr 
    -signkey client.key -out client.crt
    
    :param id_xmpp: xmpp id
    :param webid: FOAF WebId
    :type id_xmpp: string
    :type webid: string
    :param serial_number: certificate serial number
    :type serial_number: string
    :param years: number of years the certificate is going to be valid
    :type years: int
    :return: x509 self-signed certificate, key
    :rtype: tuple (X509.X509, EVP.PKey)
    
    """ 
    
    pkey = gen_keypair()
    csr = gen_csr(pkey)
    csr = set_csr_xmppwebid(csr, id_xmpp, webid)
    csr, pkey = sign_csr(pkey, csr)
    
    cert = gen_cert_from_csr(csr, serial_number, years)
    cert = set_cert_xmppwebid(cert, id_xmpp, webid)
    cert, pkey = sign_cert(pkey, cert)

    # Print the new certificate as a PEM-encoded string
    print "Generated new self-signed client certificate"
    logging.debug(cert.as_pem())

    return cert, pkey

def gen_xmppwebid_casigned_cert(cacert, capkey, id_xmpp, webid, 
                      serial_number=0, years=1):
    """Create an x509 CA-signed certificate
    
    :param id_xmpp: xmpp id
    :param webid: FOAF WebId
    :type id_xmpp: string
    :type webid: string
    :param serial_number: certificate serial number
    :type serial_number: string
    :param years: number of years the certificate is going to be valid
    :type years: int
    :return:  x509 self-signed certificate, private key
    :rtype: tuple (X509.X509, EVP.PKey)
    
    """ 
    
    pkey = gen_keypair()
    csr = gen_csr(pkey)
    csr = set_csr_xmppwebid(csr, id_xmpp, webid)
    csr, pkey = sign_csr(pkey, csr)
    
    cert = gen_cert_from_csr(csr, serial_number, years)
#    cert = set_cert_xmppwebid(cert, id_xmpp, webid)
    cert = set_casigned_cert(id_xmpp, webid, cacert, cert)
    cert, capkey = sign_cert(capkey, cert)

    # Print the new certificate as a PEM-encoded string
    print "Generated new CA certificate"
    logging.debug(cacert.as_pem())

    return cert, pkey

def gen_cacert(CN=None, C=None, O=None, OU=None, Email=None, 
               serial_number=0, years=1):
    """Create an x509 CA certificate
    
    :param serial_number: certificate serial number
    :type serial_number: string
    :param years: number of years the certificate is going to be valid
    :type years: int
    :param CN: certificate commonName
    :param C: certificate countryName
    :param O: certificate organizationName
    :param OU: certificate organizationalUnitName
    :param Email: certificate emailAddress
    :type CN: string
    :type C: string
    :type O: string
    :type OU: string
    :type Email: string
    :return: x509 self-signed certificate, key
    :rtype: tuple (X509.X509, EVP.PKey)
    
    """ 
    
    pkey = gen_keypair()
    csr = gen_csr(pkey)
    csr = set_csr_subject(csr, CN, C, O, OU, Email)
    csr, pkey = sign_csr(pkey, csr)
    
    cert = gen_cert_from_csr(csr, serial_number, years)
    cert = set_cacert(cert, CN, C, O, OU, Email)
    cert, pkey = sign_cert(pkey, cert)

    # Print the new certificate as a PEM-encoded string
    print "Generated new self-signed client certificate"
    logging.debug(cert.as_pem())

    return cert, pkey
    
def save_pkey_cert_to_pemfile(cert, pkey, cert_path='/tmp/xmppwebid_cert.pem', 
        key_path='/tmp/xmppwebid_key.key'):
    """Save cert and pkey to files
    
    :param pkey: key 
    :type pkey: EVP.PKey
    :param cert:  x509 certificate
    :type cert: X509.X509
    :param cert_path: certificate path
    :param key_path: key path
    :type cert_path: string
    :type key_path: string
    :return: x509 certificate path, key path
    :rtype: tuple (string, string)

    """
    # save key without ask for password
    pkey.save_key(key_path, None)
    cert.save_pem(cert_path)
    return cert_path, key_path

# Same using OpenSSL
#def save_pkey_cert_to_pemfile(cert, pkey, cert_path='/tmp/xmppwebid_cert.pem', 
#        key_path='/tmp/xmppwebid_key.key'):
#    """Save cert and pkey as PEM files
#    
#    :param pkey: key 
#    :type pkey: 
#    :param cert:  x509 certificate
#    :type cert: 
#    :param cert_path: certificate path
#    :param key_path: key path
#    :type cert_path: string
#    :type key_path: string
#    :return: x509 certificate path, key path
#    :rtype: tuple (string, string)

#    """
#    certdump = OpenSSL.crypto.dump_certificate(OpenSSL.SSL.FILETYPE_PEM, cert)
#    cert_file = open(cert_path, "w")
#    cert_file.write(certdump)
#    cert_file.close()
#    pkeydump = OpenSSL.crypto.dump_privatekey(OpenSSL.SSL.FILETYPE_PEM, pkey)
#    pkey_file = open(key_path, "w")
#    pkey_file.write(pkeydump)
#    pkey.close()
#    pkey_file.close()
#    return cert_path, key_path

def gen_xmppwebid_selfsigned_cert_pemfile(id_xmpp, webid, 
        cert_path='/tmp/xmppwebid_cert.pem', 
        key_path='/tmp/xmppwebid_key.key', 
        serial_path='/tmp/xmppwebid_cert_serial.txt', years=1,):
    """Create an x509 self-signed certificate and save it as PEM file
    
    :param serial_path: serial file path
    :type serial_path: string
    :param id_xmpp: xmpp id
    :param webid: FOAF WebId
    :type id_xmpp: string
    :type webid: string
    :param years: number of years the certificate is going to be valid
    :type years: int
    :param cert_path: certificate path
    :param key_path: key path
    :type cert_path: string
    :type key_path: string
    :return: x509 certificate path, key path
    :rtype: tuple (string, string)

    """
    serial_number = get_serial_from_file(serial_path)
    cert, pkey = gen_xmppwebid_selfsigned_cert(id_xmpp, webid, serial_number,
                                               years)
    save_pkey_cert_to_pemfile(cert, pkey, cert_path, key_path)
    return cert_path, key_path

def gen_xmppwebid_casigned_cert_pemfile(id_xmpp, webid, 
        cacert_path='/tmp/xmppwebid_cacert.pem', 
        cakey_path='/tmp/xmppwebid_cakey.key', 
        cert_path='/tmp/xmppwebid_cert.pem', 
        key_path='/tmp/xmppwebid_key.key', 
        serial_path='/tmp/xmppwebid_cert_serial.txt', years=1):
    """Create an x509 CA-signed certificate and save it as PEM file
    
    :param id_xmpp: xmpp id
    :param webid: FOAF WebId
    :type id_xmpp: string
    :type webid: string
    :param serial_path: serial file path
    :type serial_path: string
    :param years: number of years the certificate is going to be valid
    :type years: int
    :param cert_path: certificate path
    :param key_path: key path
    :type cert_path: string
    :type key_path: string
    :param cacert_path: certificate path
    :param cakey_path: key path
    :type cacert_path: string
    :type cakey_path: string
    :return: x509 certificate path, key path
    :rtype: tuple (string, string)

    """
    serial_number = get_serial_from_file(serial_path)
    cakey = get_pkey_from_pkeypemfile(cakey_path)
    cacert = get_cert_from_certpemfile(cacert_path)
    cert, pkey = gen_xmppwebid_casigned_cert(cacert, cakey, id_xmpp, webid, 
                                     serial_number, years)
    save_pkey_cert_to_pemfile(cert,pkey, cert_path, key_path)
    return cert_path, cakey_path


def gen_cacert_pemfile(CN=None, C=None, O=None, OU=None, Email=None, 
        cacert_path='/tmp/xmppwebid_cacert.pem', 
        cakey_path='/tmp/xmppwebid_cakey.key', 
        serial_path='/tmp/xmppwebid_cert_serial.txt', years=1):
    """Create an x509 CA certificate and save it as PEM file
    
    :param CN: certificate commonName
    :param C: certificate countryName
    :param O: certificate organizationName
    :param OU: certificate organizationalUnitName
    :param Email: certificate emailAddress
    :type CN: string
    :type C: string
    :type O: string
    :type OU: string
    :type Email: string
    :param serial_path: serial file path
    :type serial_path: string
    :param years: number of years the certificate is going to be valid
    :type years: int
    :param cacert_path: certificate path
    :param cakey_path: key path
    :type cacert_path: string
    :type cakey_path: string
    :return: x509 certificate path, key path
    :rtype: tuple (string, string)

    """
    serial_number = get_serial_from_file(serial_path)
    cert, pkey = gen_cacert(CN, C, O, OU, Email, serial_number, years)
    save_pkey_cert_to_pemfile(cert, pkey, cacert_path, cakey_path)
    return cacert_path, cakey_path

def get_pkey_from_pkeypemfile(key_path='/tmp/xmppwebid_key.key'):
    """Get key from file
    
    :param key_path: key path
    :type key_path: string
    :return: key
    :rtype: EVP.PKey

    """
#    pkey = OpenSSL.crypto.load_privatekey(OpenSSL.SSL.FILETYPE_PEM, open(key_path).read())
    priv_rsa=RSA.load_key(key_path)
    pkey=EVP.PKey()
    pkey.assign_rsa(priv_rsa)
    return pkey

def get_cert_from_certpemfile(cert_path='/tmp/xmppwebid_cert.pem'):
    """Get certificate from file
    
    :param cert_path: certificate path
    :type cert_path: string
    :return: x509 certificate
    :rtype:  X509.X509

    """
#    cert = OpenSSL.crypto.load_certificate(OpenSSL.SSL.FILETYPE_PEM, 
#                                           open(cert_path).read())
    cert=X509.load_cert(cert_path)
    return cert

def pkey_cert_2_pkcs12cert(cert, pkey):
    """Create a PKCS12 certificate from x509 certificate and key
    
    :param pkey: key 
    :type pkey: OpenSSL.crypto.PKey
    :param cert:  x509 certificate
    :type cert: OpenSSL.crypto.X509
    :return: PKCS12 certificate
    :rtype: OpenSSL.crypto.PKCS12

    .. todo::
       create pkcs12 m2crypto function 
       (http://osdir.com/ml/python.cryptography/2004-05/msg00001.html)
    .. todo::
       create pkcs12 with password interactively

    """
    p12 = OpenSSL.crypto.PKCS12()
    p12.set_privatekey(pkey)
    p12.set_certificate(cert)
    return p12

def save_pkcs12cert_to_pkcs12file(p12, p12cert_path='/tmp/xmppwebid_cert.p12'):
    """Save PKCS12 certificate to file
    
    :param p12: PKCS12 certificate
    :type p12: OpenSSL.crypto.PKCS12
    :param p12cert_path: PKCS12 certificate path
    :type p12cert_path: string
    :return: PKCS12 certificate path
    :rtype: string

    """
    p12cert = open(p12cert_path,"w")
    p12cert.write(p12.export())
    p12cert.close()
    return p12cert_path


def pemfile_2_pkcs12file(cert_path='/tmp/xmppwebid_cert.pem', 
        key_path='/tmp/xmppwebid_key.key', 
        p12cert_path='/tmp/xmppwebid_cert.p12'):
    """Create a PKCS12 certificate and save it from x509 certificate and 
    key files as PEM
    
    :param cert_path: certificate path
    :param key_path: key path
    :param p12cert_path: key path
    :type cert_path: string
    :type key_path: string
    :type p12cert_path: string
    :return: PKCS12 certificate path
    :rtype: string

    """
    # need the OpenSSL type
#    pkey = get_pkey_from_pkeypemfile(key_path)
#    cert = get_cert_from_certpemfile(cert_path)
    pkey = OpenSSL.crypto.load_privatekey(OpenSSL.SSL.FILETYPE_PEM, 
                                          open(key_path).read())
    cert = OpenSSL.crypto.load_certificate(OpenSSL.SSL.FILETYPE_PEM, 
                                           open(cert_path).read())
    p12 = pkey_cert_2_pkcs12cert(cert, pkey)
    p12cert_path = save_pkcs12cert_to_pkcs12file(p12, p12cert_path)
    return p12cert_path

def get_pkcs12cert_from_pkcs12file(p12cert_path='/tmp/xmppwebid_cert.p12'):
    """Get PKCS12 from file
    
    :param p12cert_path: key path
    :type p12cert_path: string
    :return: PKCS12 certificate
    :rtype: OpenSSL.crypto.PKCS12

    """
    p12 = OpenSSL.crypto.load_pkcs12(open(p12cert_path).read())
    return p12

def get_cert_pkey_from_pkcs12cert(p12):
    """Get X509 certificate and key from PKCS12 
    
    :param p12: PKCS12 certificate
    :type p12: OpenSSL.crypto.PKCS12
    :return: x509 self-signed certificate, key
    :rtype: tuple (OpenSSL.crypto.X509, OpenSSL.crypto.PKey)

    """
    cert = p12.get_certificate()
    pkey = p12.get_privatekey()
    return cert, pkey

def pkcs12file_2_pemfile(cert_path='/tmp/xmppwebid_cert.pem', 
        key_path='/tmp/xmppwebid_key.key', 
        p12cert_path='/tmp/xmppwebid_cert.p12'):
    """Get X509 certificate and key from PKCS12 file and save them as PEM
    key files as PEM
    
    :param cert_path: certificate path
    :param key_path: key path
    :param p12cert_path: key path
    :type cert_path: string
    :type key_path: string
    :type p12cert_path: string

    """
    p12 = get_pkcs12cert_from_pkcs12file(p12cert_path)
    cert, pkey = get_cert_pkey_from_pkcs12cert(p12)
    # need openssl types
#    save_pkey_cert_to_pemfile(cert, pkey, cert_path, key_path)
    certdump = OpenSSL.crypto.dump_certificate(OpenSSL.SSL.FILETYPE_PEM, cert)
    cert_file = open(cert_path, "w")
    cert_file.write(certdump)
    cert_file.close()
    pkeydump = OpenSSL.crypto.dump_privatekey(OpenSSL.SSL.FILETYPE_PEM, pkey)
    pkey_file = open(key_path, "w")
    pkey_file.write(pkeydump)
    pkey.close()
    pkey_file.close()
    return cert_path, key_path

def certpemfile_pkeypemfile_2_certpemfile(cert_path='/tmp/xmppwebid_cert.pem', 
        key_path='/tmp/xmppwebid_key.key',
        certkey_path='/tmp/xmppwebid_cert_key.pem'):
    """Create a PEM file with X509 certificate and key from PEM files
    
    :param cert_path: certificate path
    :param key_path: key path
    :param certkey_path: key path
    :type cert_path: string
    :type key_path: string
    :type certkey_path: string
    :return: PEM file with X509 certificate and key path
    :rtype: string

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


def get_modulus_exponent_from_certpemfile(cert_path='/tmp/xmppwebid_cert.pem'):
    """Get the modulus and exponent of RSA key from a PEM Certificate file
    
    m2.rsa_get_e(rsa.rsa) return something like '\x00\x00\x00\x03\x01\x00\x01'
    so to get the decimal value (65537), two crufty methods
    
    :param cert_path: certificate path
    :type cert_path: string
    :return: tuple(modulus, exponent)
    :rtype: tuple (hex, int)

    .. todo::
       replace the exponent method with something cleaner

    """
    cert=X509.load_cert(cert_path)
    pubkey = cert.get_pubkey()
    modulus = pubkey.get_modulus()
    
    pkey_rsa = pubkey.get_rsa()
    e  = m2.rsa_get_e(pkey_rsa.rsa)
#    exponent = int(eval(repr(e[-3:]).replace('\\x', '')),16)
    exponent = int(''.join(["%2.2d" % ord(x) for x in e[-3:]]),16)
    
    return modulus, exponent

def get_modulus_exponent_from_cert_and_pkey_pemfile(cert_path='/tmp/xmppwebid_cert.pem', 
        key_path='/tmp/xmppwebid_key.key'):
    """Get the modulus and exponent of RSA key from a PEM Certificate and
    key files
    m2.rsa_get_e(rsa.rsa) return something like '\x00\x00\x00\x03\x01\x00\x01'
    so to get the decimal value (65537), two crufty methods
    
    :param cert_path: certificate path
    :type cert_path: string
    :param key_path: key path
    :type key_path: string
    :return: tuple(modulus, exponent)
    :rtype: tuple (hex, int)

    .. TODO::
       replace the exponent method with something cleaner

    """
    cert=X509.load_cert(cert_path)
    pubkey = cert.get_pubkey()
    modulus = pubkey.get_modulus()
    
    pkey_rsa = RSA.load_key(key_path)
    e  = m2.rsa_get_e(pkey_rsa.rsa)
#    exponent = int(eval(repr(e[-3:]).replace('\\x', '')),16)
    exponent = int(''.join(["%2.2d" % ord(x) for x in e[-3:]]),16)
    
    return modulus, exponent
    
def get_modulus_exponent_from_pkcs12file():
    pass

def get_modulus_exponent_from_FOAF(foaf):
    pass
#    if type(foaf) == rdf
#    if type(foaf) == rdfa

def verify_CA_cert(cert, cacert):
    # verify
    print "Client certificate verfication with CA certificate key"
    print m2.x509_verify(cert.x509, m2.x509_get_pubkey(cacert.x509))
    
def check_csr(csr):
    pass
    #R  = csr.as_der()
    #from pyasn1.codec.der import decoder as asn1
    # a = asn1.decode(R)

def validate_xmppwebid_rsa():
    pass
    
#view certificate details: openssl x509 -in filename.crt -noout -text
