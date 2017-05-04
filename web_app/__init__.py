from config import MONGODB_DB

from flask import Flask
from flask_admin import Admin
from flask_mongoengine import MongoEngine
from flask_wtf.csrf import CSRFProtect
from flask_basicauth import BasicAuth

from helper import make_celery

import logging as lg

app = Flask(__name__)
app.config.from_object('config')

db = MongoEngine(app)

celery = make_celery(app)

admin = Admin(app, name=MONGODB_DB, template_mode='bootstrap3')

csrf = CSRFProtect(app)

basic_auth = BasicAuth(app)
# lg.info("admin_creds: \n{0}\n{1}".format(app.config['BASIC_AUTH_USERNAME'],
# app.config['BASIC_AUTH_PASSWORD']))

import web_app.routes, web_app.views
