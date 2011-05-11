#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='xmppwebid_certs',
    version='0.1',
    description='Python functions for generate a X509 client certificate for XMPP or HTTP  WebID authentication (including WebId and XMPP id at SubjectAltName).',
    author='julia',
    author_email='julia dot anaya at gmail dot com',
    url='https://xmppwebid.github.com/myceliafoafssl/wiki/XmppFoafSSL',
    download_url='git://git.xmppwebid.github.com/python-xmppwebid_certs',
    packages=find_packages(),
    include_package_data=True,

    keywords = 'python foaf ssl certificate X509 PKCS12',
    license = 'GPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

