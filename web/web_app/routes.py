import json
from web_app import app
from web_app.utils import check_token
from flask import request, make_response, redirect, url_for, render_template, flash

from helper.tasks import add_user, make_data_dirs
from web_app.forms import RegistrationForm
from web_app.models import User


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data,
                    full_name=form.full_name.data)
        user.save()
        return redirect(url_for('thanks', _external=True, _scheme='https'))
    return render_template('register.html', form=form)

@app.route('/thanks')
def thanks():
    return "Thanks, maybe this will look pretty"

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

    print(request.get_json())

    # if payload is not None:
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
