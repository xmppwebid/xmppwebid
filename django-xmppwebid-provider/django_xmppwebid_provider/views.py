#!/usr/bin/python
# vim: set expandtab tabstop=4 shiftwidth=4:
# -*- coding: utf-8 -*-

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
    views
    ~~~~~~~~

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
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import template
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from settings import JABBER_CACERT_PATH, JABBER_CAKEY_PATH, JABBER_DOMAIN, CERT_SERIAL_PATH, STATIC_URL, MEDIA_URL

from jabber_registration import JabberUtil
from socket import error as SocketError
from pyxmpp.jabber.clientstream import RegistrationError

from xmppwebid.xmppwebid import gen_xmppwebid_casigned_cert_pemfile, \
     pemfile_2_pkcs12file

from forms import XmppIdentityForm

#@csrf_protect
def xmpp_identity(request):
    """Create jabber account if it does not exist and a XMPPWebID certificate
    
    :TODO:
     * Create form for custom name and webid
     * Include in the form  the password and change xmppwebid_certs to get it from variable/file
     * Firefox should ask to import the cert instead of downloading
     * include FOAF URI in jabber vCard
     * is the password file needed or can be substitude by a dummy password to register jabber account?
    
    """
    errors = False
    messages = []
    
    if request.method == 'POST': 
        form = XmppIdentityForm(request.POST) 
        if form.is_valid(): 
            xmpp_password = form.cleaned_data['xmpp_password']
#            username, domain = id_xmpp.split('@')
            username = xmpp_user = form.cleaned_data['xmpp_user']
            domain = JABBER_DOMAIN
            # first create jabber account if it does not exists
            try:
                c = JabberUtil(username, domain, xmpp_password)
                c.register()
            # c.connect(register=True) -> Network is unreachable
            except SocketError, msg: 
                # Pass the error to template
                message = "Error trying to connect with XMPP server: " +msg[1]
                print message
                messages.append(message)
                errors = True
                # can continue download HTTP WebID certificate
            # RegistrationError: Authentication error condition: conflict
            # @TODO
            # service not available
            # Authentication error condition: conflict
            except RegistrationError, msg:
#                if str(msg)=="Authentication error condition: conflict":
                message = "Error trying to create XMPP user, that user already exists: "+str(msg)
                print message
                # Pass the error to template
                messages.append(message)
                errors = True
                # can continue download HTTP WebID certificate
            except Exception, e:
                message = "Unknown error, is the network or XMPP server running or network is propertly configured?: "+str(e)
                print message
                messages.append(message)
                errors = True
                # can continue download HTTP WebID certificate
            else:
                print "Jabber account %s@%s created" % (username, domain)
                webid = str(form.cleaned_data['webid'])
                id_xmpp = str(username)+'@'+domain
                try: 
                    #ideally would be
    #                gen_xmppwebid_selfsigned_cert_pemfile(id_xmpp, webid, serial_path=CERT_SERIAL_PATH)
                    # but jabber server still needs a CA signed certificate
                    gen_xmppwebid_casigned_cert_pemfile(id_xmpp, webid, JABBER_CACERT_PATH, JABBER_CAKEY_PATH, serial_path=CERT_SERIAL_PATH)
                    path = pemfile_2_pkcs12file()
                    print "PKC12 path: " + path
                except Exception, e:
                    message = "Error trying to generate client certificate: " + str(e)
                    print message
                    messages.append(message)
                    # can not continue
                else:
                    fp = open(path)
                    content = fp.read()
                    fp.close()
                    length = os.path.getsize(path)
                    r = HttpResponse(mimetype="application/x-x509-user-cert")
                    r['Content-Disposition'] = 'attachment; filename=%s%s' % (id_xmpp, "_cert.p12")
                    r["Content-Length"] = length
                    r["Accept-Ranges"] ="bytes"
                    r.write(content)
        #            request.user.message_set.create(message=_("You have finished creating a client certificate with webid: '%(webid)s and xmpp id: %(id_xmpp)s'") % {'webid': webid, 'id_xmpp': id_xmpp})
                    messages.append("creado")
                    return r
#            finally:
            # if exception or not is happend and no return is already executed
            return render_to_response('xmppwebid_provider/xmpp_identity.html', {
                'form': form,
                "MEDIA_URL": MEDIA_URL,
                "STATIC_URL": STATIC_URL,
                'messages': messages,
            }, context_instance=RequestContext(request))
    else:
        form = XmppIdentityForm() # An unbound form

    return render_to_response('xmppwebid_provider/xmpp_identity.html', {
        'form': form,
        "MEDIA_URL": MEDIA_URL,
        "STATIC_URL": STATIC_URL,
        'messages': messages,
    }, context_instance=RequestContext(request))


