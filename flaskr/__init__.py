import os
from flask import Flask
from flask_mysqldb import MySQL

def create_app(test_config=None):
    app = Flask (__name__, instance_relative_config=True)


    # will be migrated to config.py
    app.config.from_mapping(
        DATABASE = os.path.join(app.instance_path,'flaskr.sqlite'),
        STATIC_URL_PATH = '/static',
        SECRET_KEY = 'super secret key'
    )
    if test_config is None:
        app.config.from_pyfile('config.py',silent = True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)
    from . import routes
    app.register_blueprint(routes.bp)
    app.add_url_rule('/',endpoint='index')
    print(app.config['DATABASE'])
    print(app.config['STATIC_URL_PATH'])
    app.app_context().push()

         


    # # Clean up resources before shutting down
    # @app.teardown_appcontext
    # def teardown_appcontext(exception=None):
    #     # Clean up resources here
    #     print("Cleaning up before shutting down Flask application")

    # # Register a cleanup function using atexit
    # def cleanup():
    #     # Clean up resources here
    #     print("Cleaning up before exiting the application")
    return app
