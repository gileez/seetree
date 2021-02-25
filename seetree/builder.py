from flask import Flask
from flask_migrate import Migrate
from seetree.config import Config
from seetree.db import db


def build_app(name='app'):
    app = Flask(name)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)
    return app




