from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

cred = credentials.Certificate("secrets.json")
fa = firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)

@app.route("/fetchdata/<roomID>/<apiKey>")
def fetchData(roomID, apiKey):
    try:
        if(apiKey != os.getenv('API_KEY')):
            return "Unauthenticated"
        collection = db.collection('rooms')
        doc = collection.document(roomID)
        room = doc.get()
        if room.exists:
            return json.dumps(room.to_dict())
    except:
        return "error"

@app.route("/setpresence/<roomID>/<apiKey>")
def setHumanPresence(roomID, apiKey):
    try:
        if(apiKey != os.getenv('API_KEY')):
            return "Unauthenticated"
        collection = db.collection('rooms')
        doc = collection.document(roomID)
        doc.update({'humanPresence':True})
        return "done"
    except:
        return "error"

@app.route("/removepresence/<roomID>/<apiKey>")
def removePresence(roomID, apiKey):
    try:
        if(apiKey != os.getenv('API_KEY')):
            return "Unauthenticated"
        collection = db.collection('rooms')
        doc = collection.document(roomID)
        doc.update({'humanPresence':False})
        return "done"
    except:
        return "error"

if __name__ == '__main__':
    app.run()


