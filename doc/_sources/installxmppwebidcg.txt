.. _ref-installxmppwebidcg:

================================================================
Installing django-xmppwebid-provider in Debian/Ubuntu
================================================================

Install requirements
======================

If not already installed you should install other dependencies first::

    $ sudo aptitude install python-setuptools libxml2-dev swig
    $ sudo easy_install pip
    $ sudo pip install virtualenv

If you plan to deploy the application with Apache and wsgi, install too::

    $ sudo aptitude install apache2 libapache2-mod-wsgi

Download django-xmppwebid-provider
=======================================
You can download this project in either
* `zip`_ or
* `tar`_ formats.
 
You can also clone the project with `Git`_ by running::

    $ git clone git://github.com/xmppwebid/xmppwebid
    
Create a virtualenv
===================

Create a virtualenv (you can choose any path to install the virtualenv)::

    $ virtualenv --no-site-packages /path/to/xmppwebidenv -p python2.6

Activate the virtualenv and install dependencies::

    $ source /path/to/xmppwebidenv/bin/activate
    (xmppwebidenv)$ pip install -E xmppwebidenv -r /path/to/xmppwebid/django-xmppwebid-provider/example_xmppwebid_provider/requirements

Customize the settings
=======================

Modify the settings in /path/to/xmppwebid/django-xmppwebid-provider/examples_xmppwebid_provider/settings_local.py, according to your Jabberd server and location of your certfificates (generated in the way described in :ref:`ref-certificates`::

    JABBER_DOMAIN = 'yourxmppdomain.com'
    JABBER_CACERT_PATH = os.path.join(PROJECT_ROOT, 'ca-cert.pem')
    JABBER_CAKEY_PATH = os.path.join(PROJECT_ROOT, 'ca-key.pem')
    CERT_SERIAL_PATH = os.path.join(PROJECT_ROOT, 'xmpp_foaf_cert_serial.txt')


Run the web application
========================

In the django project directory run the development server::

    (xmppwebidenv)$ cd /path/to/xmppwebid/django-xmppwebid-provider/example_xmppwebid_provider/
    (xmppwebidenv)$ python manage.py runserver

Point your browser at http://localhost:8000/

Serve the web application with Apache
======================================
  
#. Install apache following the process described above
       
#. Copy the configuration file and edit it depending on your system::

    $ cp deploy/django_xmppwebid_provider.apache /etc/apache2/sites-available/xmppwebiddomain.com

#. Enable the site and reload Apache::

    $ sudo a2ensite /etc/apache2/sites-available/xmppwebiddomain.com
    $ sudo /etc/init.d/apache2 reload

#. Remember to add to /etc/apache2/mods-enabled/mod_wsgi.conf to enable HTTP 

Create your user XMMPWebID certificate
=======================================
Once you have your app up and running , it should be pretty straightforward to generate your client cert:

Choose a user name.
Optionally, fill up to your WebID (foaf editor should be integrated into the app soon).
... If everything went fine, you should have manually generated or downloaded your freshly generated client certificate, signed by your CA, containing your JabberID (id-on-xmppAddr) and pointing to your WebID.
