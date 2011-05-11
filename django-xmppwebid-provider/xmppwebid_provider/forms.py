from django import forms
from settings import JABBER_DOMAIN
from django.utils.safestring import mark_safe
"""
@TODO: Fix max_length
 * is the password file needed or can be substitude by a dummy password to register jabber account?
"""

class CharNotEditableWidget(forms.Widget):
    def render(self, name, value, attrs):
        final_attrs = self.build_attrs(attrs, name=name)
        if hasattr(self, 'initial'):
            value = self.initial
        return mark_safe(
            "@%s" % (
                value
            )
        )
    def _has_changed(self, initial, data):
        return False


class XmppIdentityForm(forms.Form):
    xmpp_user = forms.CharField(max_length=255)
    xmpp_domain = forms.CharField(max_length=255, initial = JABBER_DOMAIN, widget = CharNotEditableWidget, required=False)
    xmpp_password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=255)
    webid = forms.URLField(required=False)

