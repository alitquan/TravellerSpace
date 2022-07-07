from __init__ import app
import os
TESTING = True
DEBUG = True
FLASK_ENV = 'deve:lopment'
SECRET_KEY = 'dev'
DATABASE = os.path.join(app.instance_path,'flaskr.sqlite')
