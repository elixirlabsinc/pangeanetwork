""" An intermediary bootstrapping file that makes factories of various reusable app components. """

import os
import typing as t

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models import db



def app_factory(config: t.Optional[t.Dict[str, t.Any]] = None) -> Flask:
    """ Bootstraps a Flask application and adds dependencies to the resulting object.

    After bootstrap, it's a good idea to never import from `run` or the source of the bootstraped
    Flask application. Instead, all boostrapped extensions should be accessed with Flask's `current_app`.

    Example:
        from flask import current_app as app

        ...

        def my_method():
            with app.appcontext():
                result = app.db.session.query(MyModel).first()

    Args:
        config (Optional[Dict[str, Any]]): A configuration object to update the app's config with

    Returns:
        Flask: The bootstrapped flask application object
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = bool(
        os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", 0)
    )
    app.config["DEBUG"] = True
    app.config.update(**(config or {}))
    app.db = database_factory(app)
    return app


def database_factory(app: Flask) -> SQLAlchemy:
    """ Bootstraps SQLAlchemy for use with the Flask-SQLAlchemy extension. 
    
    Override this method with another db factory if you'd prefer, just be
    sure to update the return typing of the `database_factory` method.

    Args:
        app (Flask): The flask app to add this db engine to

    Returns:
        SQLAlchemy: The SQLAlchemy engine
    """
    db.init_app(app)
    return db
