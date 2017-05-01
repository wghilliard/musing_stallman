import json
from web_app import app
from web_app.utils import check_token
from flask import request, make_response

from helper.tasks import add_user, make_data_dirs


@app.route('/')
def meow():
    return 'Hello, World!'


@app.route('/api/hello', methods=['POST'])
def hello():
    """
    hello should:
    - verify the incoming data from the google web form
    - set off a celery task to
        - add user to LDAP
        - create dirs
        - email user w/ creds

    :return: 200, regardless
    """

    payload = request.get_json()

    # {
    #     "api_key": "f073651b-40c4-4dd5-8172-57a4829f99a3",
    #     "name": "Bird Person",
    #     "username": "bperson",
    #     "email": "bird.person@squanch.com"
    # }

    try:
        api_key = payload['api_key']

        if check_token(api_key):
            # TODO tasks

            tmp = add_user(payload.get('name'), payload.get('username'), payload.get('email'))
            #
            make_data_dirs(*tmp)

            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False,
                               'error': 'api_key expired'}), 400, {'ContentType': 'application/json'}

    except KeyError:
        return json.dumps({'success': False,
                           'error': 'api_key required'}), 400, {'ContentType': 'application/json'}

    except Exception as e:
        print(e)
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}
