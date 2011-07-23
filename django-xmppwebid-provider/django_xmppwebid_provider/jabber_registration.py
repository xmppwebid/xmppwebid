"""
 Modified version (remaining only the code to the in-band registration scope)
 of http://www.helpim.org/browser/stable/HelpIM/jabberutils.py
 http://www.helpim.org/browser/attic/version_2/HelpIM/jabberutils.py?rev=622&format=raw
 @license: GPL (see http://www.helpim.org/)
"""

import pyxmpp.all
import pyxmpp.jabber.all
import pyxmpp.jabber.vcard
from pyxmpp.jabber.clientstream import LegacyAuthenticationError, RegistrationError

RESOURCE = "xmppwebid"

VCARD_DATA = """BEGIN:vCard
VERSION:3.0
N:%(username)s
END:vCard"""

class JabberUtil(pyxmpp.jabber.client.JabberClient):

    def __init__(self, username, server, password, nickname=None):
        # First set some constants
        self.timeout = 2
        self.resource = RESOURCE
        # Set default vCard content
        self.vCard_data = VCARD_DATA  % {"username": username}
        # Set the nickname
        if nickname:
            self.nickname = nickname
        else:
            self.nickname = username
        # initialize a jabber client
        jid = pyxmpp.jid.JID(username, server, self.resource)
        pyxmpp.jabber.client.JabberClient.__init__(self, jid, password)
        print "Initialized client with jid %s" % jid

    def loop_until_handled(self, timeout=None):
        if not timeout:
            timeout = self.timeout
        while self.stream is not None and \
              not self.stream.eof and \
              self.stream.socket is not None:
            try:
                act=self.stream.loop_iter(timeout)
            except LegacyAuthenticationError:
                return
            if not act:
                self.stream.idle()
                return
        return

    def register(self, user_list=None, disconnect=True):
        """Handle in-band registration and set vCard. """
        self.connect(register=True)
        self.loop_until_handled()
        self.disconnect()
        self.loop_until_handled()

        # And set the vCard too
        vcard = pyxmpp.jabber.vcard.VCard(self.vCard_data)
        iq = pyxmpp.iq.Iq(stanza_type='set')
        iq.set_content(vcard)
        self.connect()
        self.loop_until_handled()
        self.stream.send(iq)
        self.loop_until_handled()
        if disconnect:
            self.disconnect()
            self.loop_until_handled()
        return

