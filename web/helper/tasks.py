from web_app import celery
from web_app.models import User
import uuid, os
from ldap3 import Connection, Server, ALL
from config import LDAP_USER_DOMAIN, LDAP_GROUP_DOMAIN, DATA_VOLUMES, LDAP_HOST

import logging as lg


# @celery.task()
def add_user(full_name, username, email, pk=None):
    """
    Passwords are in cleartext sooo change them quick pls
    
    :param full_name: Bird Person
    :param username: bperson
    :param email: bird.person@squanch.com
    :return: username, new_user.uid_number, pwd_holder
    """

    # check for username already in use
    ldap_conn = get_ldap_connection()
    mongo_conn = get_mongo_connection()

    if not username_open(username, ldap_conn):
        username = username + str(int(uuid.uuid4()))[:3]
 #   else:
 #       username = "{0}{1}".format(full_name.lower().replace(' ', ''), str(int(uuid.uuid4()))[:3])[:32]

    username = username[:32]  # max linux username length of 32 characters, super redudant double check for security

    try:
        if pk is not None:
            new_user = User.objects(pk=pk).first()
            #     sanity check
            if new_user is not None:
                new_user.uid_number = get_next_uid_number(ldap_conn)
                new_user.username = username
            else:
                lg.error("cannot create new user from existing user (pk={0})".format(pk))
        else:
            new_user = User(username=username, full_name=full_name, email=email,
                            uid_number=get_next_uid_number(ldap_conn))
    except Exception as e:
        lg.error(e)
        return
    finally:
        mongo_conn.close()

    pwd_holder = generate_password()

    ldap_conn.add('uid={0},{1}'.format(new_user.username, LDAP_USER_DOMAIN), 'account',
                  {'uid': new_user.username,
                   'cn': new_user.username,
                   'homeDirectory': '/home/{0}'.format(new_user.username),
                   'uidNumber': new_user.uid_number,
                   'gidNumber': new_user.uid_number, 'objectClass': ['shadowAccount', 'posixAccount'],
                   'userPassword': pwd_holder,
                   'loginShell': '/bin/bash'
                   })

    ldap_conn.add('cn={0},{1}'.format(new_user.username, LDAP_GROUP_DOMAIN), 'posixGroup',
                  {'gidNumber': new_user.uid_number})

    new_user.password = pwd_holder

    new_user.save()

    return username, new_user.uid_number, pwd_holder


# @celery.task()
def make_data_dirs(username, uid_number):
    # TODO potentially unsafe?
    for volume in DATA_VOLUMES:
        try:
            path = os.path.abspath(os.path.join(volume, username))
            os.makedirs(path, exist_ok=True)
            os.chown(path, uid=uid_number, gid=uid_number)
        except OSError as e:
            lg.error(e)
        except Exception as e:
            lg.error(e)

    return


# TODO
def email_user(username, pwd, email, full_name):
    import yagmail
    from secrets import GMAIL_USERNAME, GMAIL_PASSWORD
    text = "\n".join(["Hello {0}".format(full_name),
                      "",
                      "Your username is: {0}".format(username),
                      "",
                      "Your password is: {0}".format(pwd),
                      "",
                      "You can connect to our services by running the following command:",
                      "`ssh -NfL 8000:127.0.0.1:8000 {0}@orodruin.uta.edu`".format(username),
                      "",
                      "Note: Please change your password ASAP, if you lose it I don't have the ability to help!"
                      # " _   _ _____  _         _   _ _____ ____       ____  _     ",
                      # "| | | |_   _|/ \       | | | | ____|  _ \     |  _ \| |    ",
                      # "| | | | | | / _ \ _____| |_| |  _| | |_) |____| | | | |    ",
                      # "| |_| | | |/ ___ \_____|  _  | |___|  __/_____| |_| | |___ ",
                      # " \___/  |_/_/   \_\    |_| |_|_____|_|        |____/|_____|"
                      ])
    try:
        yagmail.SMTP(GMAIL_USERNAME, GMAIL_PASSWORD).send(email, "UTA-HEP-DL Account Info",
                                                          text)
        return True
    except Exception as e:
        lg.exception(e)
        return False


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
    ldap_conn.search(LDAP_USER_DOMAIN, '(objectclass=posixAccount)', attributes=['uidNumber'])
    return int(max(ldap_conn.entries, key=lambda x: int(x.uidNumber.raw_values[0])).uidNumber.raw_values[0]) + 1
