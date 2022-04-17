import os
from flask import Flask

def create_app(test_config=None):
    app = Flask (__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path,'flaskr.sqlite')
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
    
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import routes
    app.register_blueprint(routes.bp)
    app.add_url_rule('/',endpoint='index')
    return app