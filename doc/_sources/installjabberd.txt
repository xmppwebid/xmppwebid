.. _ref-installjabberd:

================================================================
Installing Jabberd2 in Debian/Ubuntu
================================================================

Install Jabberd2 from the source code
======================================

A `patch`_
by Michal Witkowski (on 2009-07-27) adds support for C2S SASL External 
Authentication to jabberd2  has been merged in the 2.2.12 release.

Get the latest release::

    $ wget http://codex.xiaoka.com/pub/jabberd2/releases/jabberd-2.2.13.tar.bz2

Install the required libraries::

    $ sudo aptitude install build-essential mysql-server libmysqlclient-dev libexpat1-dev libidn11-dev libudns-dev libgsasl7-dev

Uncompress Jabberd2::

    $ tar -xvjf jabberd-2.2.13.tar.bz2

Compile it::

    $ cd jabberd-2.2.13
    $ ./configure --enable-mysql --enable-ssl
    $ make
    $ sudo make install
    
Configure Jabberd2 
=====================

Copy the certificates generated in :ref:`ref-certificates` to the Jabberd2 configuration directory::

    $ cp /path/to/my/ca/xmpp_ca_cert.pem /etc/jabberd2
    
Edit the file in /etc/jabberd2/c2s.xml. 

On <local> section comment the following line::

    <!--<id register-enable='true'>localhost.localdomain</id>-->
    And add these others:

        <id realm='yourxmppdomain.com'
            pemfile='/etc/jabberd2/myjabberdcert.pem'
            verify-mode='7'
            cachain='/etc/jabberd2/xmpp_ca_cert.pem'
            register-enable='true'
        >yourxmppdomain.com</id>

Where cachain is the CA cert you just generated, pemfile is the server certificate that will be used for client connections. 
From the documentation in c2s.xml:

"The certificates must be in PEM format and must be sorted starting with the subject's certificate (actual client or server certificate), followed by intermediate CA certificates if applicable, and ending at the highest level (root) CA" (the latter one being optional).

You could also use the following directives to give human-readable information and point to the webapp that will handle the cert creation::

      instructions='Go to http://example.org/register to get your account.'
      register-oob='http://example.org/register'

Some lines below, specify again your certificate and ca-chain, and set verify mode to 7::

    <pemfile>/etc/jabberd2/myjabberdcert.pem</pemfile>
    <verify-mode>7</verify-mode>
    <cachain>/etc/jabberd2/xmpp_ca_cert.pem</cachain>
    
Modify <authreg> section according to what database you want to use. We are going to use sqlite instead of mysql, for simplicity's sake::

    <!--<module>mysql</module>-->
    <module>sqlite</module>
    
Create the database tables::

    gunzip -c /usr/share/doc/jabberd2/db-setup.sqlite.gz  > /tmp/db-setup.sqlite
    sudo sqlite3 /var/lib/jabberd2/sqlite.db <  /tmp/db-setup.sqlite
    chown jabber:jabber /var/lib/jabberd2/sqlite.db

Finally, check that sasl-external is being offered in the ssl-mechanism section (and maybe you want to disable "plain").

Now we change a couple of things in the session manager config /etc/jabberd2/sm.xml::

    <id>yourxmppdomain.com</id>

And modify also the storage backend::

  <!-- Storage database configuration -->
  <storage>
    (...)
    <!-- By default, we use the MySQL driver for all storage -->
    <driver>sqlite</driver>
    
... and restart your server::

    /etc/init.d/jabberd2 restart

.. _patch: https://bugs.launchpad.net/jabberd2/+bug/405233
