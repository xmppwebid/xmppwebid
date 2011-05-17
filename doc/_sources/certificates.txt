.. _ref-certificates:

==========================
Creating the certificates
==========================

The server certificate that Jabberd will present to the client, does not need
to be signed by a Certification Authority (CA), it can be a self-signed 
certificate.

However, the SASL EXTERNAL authentication mechanism needs the user certificates
to be signed by a CA.

Currently Jabberd2 does not support the proposed SASL EXTERNAL WEBID. Therefore,
you will need to create a CA certificate that will be used to generate the user
certificates by the xmppwebid certificate generator and by Jabberd2 itself to
validate those user certificates. 

Download the application
========================
You can download this project in either
 * `zip`_ or
 * `tar`_ formats.
 
You can also clone the project with `Git`_ by running::

    $ git clone git://github.com/xmppwebid/xmppwebid


Create a CA certificate
------------------------

Generate the CA certificate::

    $ cd xmppwebid/python-xmppwebid-certs/xmppwebid_certs
    $ ./gen_cacert.py -h # to see the options
    $ ./gen_cacert.py #without arguments will put the CA certificate and private key in /tmp
    
Note: if you enter arguments with spaces, remember to enclose them in ' " ', or it will fail silently. Also, remember to chmod 400 your key and chown it to the jabberd user that will access to it.

Create the Jabberd2 certificate
--------------------------------

Self-signed::

    openssl genrsa 2048 > myjabberdcert.key
    openssl req -new -x509 -nodes -sha1 -days 365 -key myjabberdcert.key > myjabberdcert.cert
    cat myjabberdcert.key myjabberdcert.cert > myjabberdcert.pem && rm myjabberdcert.key
    chown jabber: myjabberdcert.pem
    chmod 400 myjabberdcert.pem
    mv myjabberdcert.pem  /etc/jabberd2/

CA-signed::
    $   

.. _zip: http://github.com/xmppwebid/xmppwebid/zipball/master
.. _tar: http://github.com/xmppwebid/xmppwebid/tarball/master
.. _Git: http://git-scm.com


