.. _ref-certificates:

==============================================
Creating certificates with python-xmppwebid
==============================================

The server certificate that Jabberd will present to the client, does not need
to be signed by a Certification Authority (CA), it can be a self-signed 
certificate.

However, the SASL EXTERNAL authentication mechanism needs the user certificates
to be signed by a CA.

Currently Jabberd2 does not support the proposed SASL EXTERNAL WEBID. Therefore,
you will need to create a CA certificate that will be used to generate the user
certificates by the xmppwebid certificate generator and by Jabberd2 itself to
validate those user certificates. 

Download python-xmppwebid
===========================
You can download this project in either
* `zip`_ or
* `tar`_ formats.
 
You can also clone the project with `Git`_ by running::

    $ git clone git://github.com/xmppwebid/xmppwebid


Create a CA certificate
===========================

Generate the CA certificate::

    $ cd xmppwebid/python-xmppwebid/xmppwebid
    $ ./create_ca.py -h # to see the options
    $ ./create_ca.py #without arguments will put the CA certificate and private key in /tmp
    
Note: if you enter arguments with spaces, remember to enclose them in ' " ', or it will fail silently. 

Create the Jabberd2 certificate
=================================

CA-signed::

    $ cd xmppwebid/python-xmppwebid/xmppwebid
    $ ./create_xmppwebid_casigned_cert.py 

Self-signed::

    $ cd xmppwebid/python-xmppwebid/xmppwebid
    $ ./create_xmppwebid_selfsigned_cert.py   

In any case, chown the certificates and key to the jabberd user that will access to it::

    chown jabber: myjabberdcert.pem
    chmod 400 myjabberdcert.pem

.. _zip: http://github.com/xmppwebid/xmppwebid/zipball/master
.. _tar: http://github.com/xmppwebid/xmppwebid/tarball/master
.. _Git: http://git-scm.com


