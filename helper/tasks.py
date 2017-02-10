from web_app import celery
from web_app.models import User
import uuid, os
from ldap3 import Connection, Server, ALL
from config import LDAP_USER_DOMAIN, LDAP_GROUP_DOMAIN, DATA_VOLUMES, LDAP_HOST


# @celery.task()
def add_user(full_name, username, email):
    """
    :param full_name: Grayson
    :param username: cats
    :param email: grayson@cats.com
    :return:
    """

    # check for username already in use
    ldap_conn = get_ldap_connection()
    mongo_conn = get_mongo_connection()

    if not username_open(username, ldap_conn):
        username = "{0}{1}".format(full_name.lower().replace(' ', ''), str(int(uuid.uuid4()))[:3])

    username = username[:32]  # max linux username length of 32 characters

    try:
        new_user = User(username=username, full_name=full_name, email=email, uid_number=get_next_uid_number(ldap_conn))
    except Exception as e:
        print(e)
        return
    finally:
        mongo_conn.close()

    ldap_conn.add('uid={0},{1}'.format(new_user.username, LDAP_USER_DOMAIN), 'account',
                  {'uid': new_user.username,
                   'cn': new_user.username,
                   'homeDirectory': '/home/{0}'.format(new_user.username),
                   'uidNumber': new_user.uid_number,
                   'gidNumber': new_user.uid_number, 'objectClass': ['shadowAccount', 'posixAccount'],
                   'userPassword': generate_password(),
                   'loginShell': '/bin/bash'
                   })

    ldap_conn.add('cn={0},{1}'.format(new_user.username, LDAP_GROUP_DOMAIN), 'posixGroup',
                  {'gidNumber': new_user.uid_number})

    new_user.save()

    return username, new_user.uid_number


# @celery.task()
def make_data_dirs(username, uid_number):
    # TODO potentially unsafe?
    for volume in DATA_VOLUMES:
        try:
            path = os.path.abspath(os.path.join(volume, username))
            os.makedirs(path, exist_ok=True)
            os.chown(path, uid=uid_number, gid=uid_number)
        except OSError as e:
            print(e)
        except Exception as e:
            print(e)

    return


# TODO
def email_user():
    return


def get_mongo_connection():
    from mongoengine import connect
    from config import MONGODB_DB, MONGODB_HOST, MONGODB_PORT

    db = connect(MONGODB_DB, host=MONGODB_HOST, port=MONGODB_PORT)

    return db


def get_ldap_connection():
    # TODO Need better way?
    from secrets import LDAP_KEY, LDAP_USER
    server = Server(LDAP_HOST, get_info=ALL)
    return Connection(server, LDAP_USER, LDAP_KEY, auto_bind=True)


def generate_password():
    return str(uuid.uuid4()).replace('-', '')[5:20]


def username_open(username, ldap_conn):
    ldap_conn.search(LDAP_USER_DOMAIN, '(&(objectclass=account)(uid={0}))'.format(username))

    if len(ldap_conn.entries) > 0:
        return False
    else:
        return True


def get_next_uid_number(ldap_conn):
    # black magic
    # (∩｀-´)⊃━☆ﾟ.*･｡ﾟ

    ldap_conn.search(LDAP_USER_DOMAIN, '(objectclass=posixAccount)', attributes=['uidNumber'])
    return int(max(ldap_conn.entries, key=lambda x: int(x.uidNumber.raw_values[0])).uidNumber.raw_values[0]) + 1
