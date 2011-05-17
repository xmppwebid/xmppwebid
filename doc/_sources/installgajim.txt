.. _ref-installgajim:

=======================================
Install Gajim and the user certificate
=======================================

Thanks to a `patch`_ that has been integrated in the trunk, Gajim v0.14 supports 
the C2S SASL External authentication. 

Install Gajim from the source code
====================================

Install the user certificate into the client
=============================================

First, we should add our new account:

"Edit" -> "Accounts" -> "Add -> "I already have an account I want to use."

Fill with the data of the account we just registered in the web app. We can leave the password field empty, since it is not going to be used.

Uncheck "connect when I press Finish"

Click on "Advanced" button.

Next, let's set the certificate for this account:

In the "Account" tab, expand the "Client Certificate" item at the bottom.

Choose your Client Cert from the path where you saved it (watch out for permissions, since it does not have the private key encrypted! ).

Unmark the "Enable" tickbox at the top, and mark it again. Close the window, and set your status to Available to connect.

Et voila! You should be connecting to your jabber server passwordless :)

In case of trouble, open a ticket or contact at info at rhizomatik.net.

