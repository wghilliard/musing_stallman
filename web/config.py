import os

PREFERRED_URL_SCHEME = 'https'

MONGODB_HOST = os.environ.get('MONGODB_HOST', default='192.168.1.30')
MONGODB_PORT = os.environ.get('MONGODB_PORT', default=27017)
MONGODB_DB = 'musing_stallman'

CELERY_BROKER_URL = 'pyamqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'rpc://guest:guest@localhost:5672//'

LDAP_HOST = os.environ.get('LDAP_HOST', default='192.168.1.30')
LDAP_PORT = os.environ.get('LDAP_PORT', default=389)
LDAP_USER_DOMAIN = 'ou=People,dc=utadl,dc=org'
LDAP_GROUP_DOMAIN = 'ou=Group,dc=utadl,dc=org'

DATA_VOLUMES = ['/data', '/scratch']

try:
    from secrets import BASIC_AUTH_PASSWORD, BASIC_AUTH_USERNAME
except ImportError:
    import uuid

    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD', default=str(uuid.uuid4()))
    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME', default="admin")

try:
    from secret_key import SECRET_KEY
except ImportError:
    # Create missing secret key
    import random
    import string
    import os

    SECRET_KEY = ''.join([random.choice(string.ascii_letters) for x in range(64)])
    with open(os.path.join(os.getcwd(), 'secret_key.py'), 'w+') as key_file:
        key_file.write("SECRET_KEY = '%s'" % SECRET_KEY)
        key_file.flush()
