import os.path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

JABBER_DOMAIN = 'yourxmppdomain.com'
JABBER_CACERT_PATH = os.path.join(PROJECT_ROOT, 'ca-cert.pem')
JABBER_CAKEY_PATH = os.path.join(PROJECT_ROOT, 'ca-key.pem')
CERT_SERIAL_PATH = os.path.join(PROJECT_ROOT, 'xmppwebid_cert_serial.txt')
