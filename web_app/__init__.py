from config import MONGODB_DB

from flask import Flask
from flask_admin import Admin
from flask_mongoengine import MongoEngine

from helper import make_celery

app = Flask(__name__)
app.config.from_object('config')

db = MongoEngine(app)

celery = make_celery(app)

admin = Admin(app, name=MONGODB_DB, template_mode='bootstrap3')

import web_app.routes, web_app.views
