from flaskr import create_app
from flaskr.db import  testThread
from flask_socketio import SocketIO


app = create_app()
socketio = SocketIO(app,cors_allowed_origins="*")

from events import *

if __name__ == "__main__":
    print ("Hello")
    socketio.run(app,debug=True)
