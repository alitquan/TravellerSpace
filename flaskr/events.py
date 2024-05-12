from .extensions import socketIO 

@socketIO.on("connect") 
def handle_connect():
    print ("Client connected") 
