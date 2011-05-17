.. _ref-introduction:

=================
About XMPPWebID 
=================

XMPPWebID is an project intended to add `WebID`_ authentication to the `XMPP`_ 
protocol.


Technologies
============

 * XMPP protocol
 * WebID for authentication
 * `FOAF`_ ontology for the user WebID profile
 * `Certificate`_ and `RSA`_ vocabularies to associate the user certificate public key to the WebID
 * `X509`_ certificates
 * XMPP `In-Band-Registration`_ extension for account registration
 * `TLS`_ protocol for secure communications
 * XMPP `SASL EXTERNAL`_ authentication mechanism
 * `SPARQL`_ to extract WebID URI, public keys and Jabber account

XMPPWebID certificate generator
================================

XMPPWebID certificate generator is an `Django`_ app intended to generate valid
certificates for HTPP and XMPP.
    
It creates XMPP account and generates the certificate that is installed in your 
browser and can also be installed in a XMPP client.

To use your certificate in XMPP (Jabber) you would need a client that supports
user certificates (currently `Gajim`_ v0.14) and a Jabber server software that 
supports SASL EXTERNAL authentication (`Jabberd`_).


Install
--------
To install XMPPWebID  certificate generator see :ref:`ref-install`

Download
=========
You can download this project in either
 * `zip`_ or
 * `tar`_ formats.
 
You can also clone the project with `Git`_ by running::
    $ git clone git://github.com/xmppwebid/xmppwebid

Bugs and features
=================
If you wish to signal a bug or report a feature request, please fill-in an issue on the `XMPPWebID issue tracker`_

License
=======
XMPPWebID is copyright 2010 by xmppwebid 
and is covered by the `GPLv3`_

Contact
========
(xmppwebid at gmail dot com)

Acknowledgments
================
`foaf-protocols`_ community 




.. _WebID: http://www.w3.org/2005/Incubator/webid/spec/
.. _XMPP: http://xmpp.org/
.. _SPARQL: http://www.w3.org/TR/rdf-sparql-query/
.. _FOAF: http://xmlns.com/foaf/spec/
.. _Django: http://djangoproject.com/
.. _Gajim: http://gajim.org/
.. _SASL EXTERNAL: http://xmpp.org/extensions/xep-0178.html
.. _Jabberd: http://codex.xiaoka.com/wiki/jabberd2:start 
.. _zip: http://github.com/xmppwebid/xmppwebid/zipball/master
.. _tar: http://github.com/xmppwebid/xmppwebid/tarball/master
.. _XMPPWebID issue tracker: https://github.com/xmppwebid/xmppwebid/issues
.. _Git: http://git-scm.com
.. _GPLv3: http://git-scm.com
.. _In-Band-Registration: http://xmpp.org/extensions/xep-0077.html
.. _TLS: http://tools.ietf.org/html/rfc5246
.. _Certificate: http://www.w3.org/ns/auth/cert
.. _RSA:  http://www.w3.org/ns/auth/rs
.. _X509: http://www.itu.int/rec/T-REC-X.509/en
.. _foaf-protocols: http://lists.foaf-project.org/mailman/listinfo/foaf-protocols
