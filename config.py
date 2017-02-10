# TODO get config from env variable

MONGODB_HOST = 'localhost'
MONGODB_PORT = int(27017)
MONGODB_DB = 'musing_stallman'

CELERY_BROKER_URL = 'pyamqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'rpc://guest:guest@localhost:5672//'

LDAP_HOST = 'localhost'
LDAP_PORT = 389
LDAP_USER_DOMAIN = 'ou=People,dc=utadl,dc=org'
LDAP_GROUP_DOMAIN = 'ou=Group,dc=utadl,dc=org'

DATA_VOLUMES = ['/data', '/scratch']

from secrets import SECRET_KEY

# TODO influx tracking?
