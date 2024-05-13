import pymongo
from app import socketio 
from flaskr.db import getMessagesCollection 
from flaskr.routes import getUsername
from threading import Thread
from flask import request

client = pymongo.MongoClient("localhost", 27017)
messages = getMessagesCollection() 

running_threads = {}

def watch_messages(sid): 
 # Subscribe to changes in MongoDB collection
    change_stream = messages.watch(full_document='updateLookup')
    for change in change_stream:
        new_message = change['fullDocument']
        body = new_message['body']
        id   = new_message['userID']

        
        socketio.emit('new_message', {'msg':body,'userID':id} , room=sid)
        print(id, " - says - ", body)
   

@socketio.on('connect') 
def handle_connect():
    sid = request.sid
 # Start a new thread to watch for messages
    t = Thread(target=watch_messages, args=(sid,))
    t.start()

    # Store the thread in the dictionary
    running_threads[sid] = t
    print("handle_connected")

@socketio.on('disconnect')
def handle_disconnect():

    sid = request.sid

    t = running_threads.pop(sid, None)
    if t:
        t.join()  # Wait for the thread to finish
        print("Thread stopped")
    print('Client disconnected')

@socketio.on('ding')
def handle_ding(data):  # Accept data argument
    print("Received ding event with data:", data)

