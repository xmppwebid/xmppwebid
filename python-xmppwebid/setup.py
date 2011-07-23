#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='xmppwebid',
    version='0.2',
    description='Python functions to generate X509 certificates valid for XMPP or HTTP  WebID authentication.',
    author='Julia Anaya',
    author_email='julia dot anaya at gmail dot com',
    url='https://xmppwebid.github.com/xmppwebid',
    download_url='https://github.com/janaya/xmppwebid/tarball/master',
    packages=find_packages(),
    include_package_data=True,

    keywords = 'python webid XMPP foaf ssl certificate X509 PKCS12',
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

