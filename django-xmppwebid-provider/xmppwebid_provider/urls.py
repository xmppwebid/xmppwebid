from django.conf.urls.defaults import *

urlpatterns = patterns('',
#    url(r'^$', 'xmppwebid_provider.views.gen_cert', name='gen_cert'),
    url(r'^$', 'xmppwebid_provider.views.xmpp_identity', name='xmpp_identity'),
)


