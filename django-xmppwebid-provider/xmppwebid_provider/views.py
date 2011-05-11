from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import template
from  xmppwebid_certs.xmpp_foaf_cert import *
from datetime import datetime
from forms import *
from settings import JABBER_CACERT_PATH, JABBER_CAKEY_PATH, JABBER_DOMAIN, CERT_SERIAL_PATH, STATIC_URL, MEDIA_URL
from django.utils.translation import ugettext_lazy as _

from jabber_registration import JabberUtil
from socket import error as SocketError
from pyxmpp.jabber.clientstream import RegistrationError

def xmpp_identity(request):
    """
    create jabber account if it does not exits..
    @TODO:
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
            # Process the data in form.cleaned_data
#            id_xmpp = form.cleaned_data['id_xmpp']
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
    #            mkcert_casigned_from_file_save(str(id_xmpp), str(webid), JABBER_CACERT_PATH, JABBER_CAKEY_PATH)
                id_xmpp = str(username)+'@'+domain
                mkcert_casigned_from_file_save(id_xmpp, webid, JABBER_CACERT_PATH, JABBER_CAKEY_PATH, serial_path=CERT_SERIAL_PATH)
    #            if 'PEM' in request.POST:
    #                path = pemcert()
    #            elif 'PKCS12' in request.POST:
                try: 
                    path = pkcs12cert()
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


