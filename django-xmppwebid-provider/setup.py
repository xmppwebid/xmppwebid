#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages
import os

VERSION = __import__('xmppwebid_provider').__version__

def read(*path):
    return open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *path)).read()

setup(
    name='xmppwebid_provider',
    version=VERSION,
    description='Django app  intended to generate valid certificates for HTPP and XMPP WebID authentication',
    long_description=read('docs', 'intro.txt'),
    author='Duy',
    author_email='julia dot anaya@ gmail dot com',
    download_url='https://github.com/xmppwebid/xmppwebid.git',
    url='http://xmppwebid.github.com/xmppwebid',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Framework :: Django',
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='foaf, ssl, webid, xmpp, x509, certificate, client certificate, authentication, authorization,django',
    include_package_data=True,
    zip_safe=False,
    exclude_package_data={
        'requirements': ['%s/*.tar.gz' % VERSION],
    },

)

