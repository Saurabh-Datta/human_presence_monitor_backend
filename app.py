from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
from flask_mail import Mail, Message

cred = credentials.Certificate("secrets.json")
fa = firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_ID')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PWD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

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

@app.route("/switchon/<roomID>/<apiKey>")
def turnOnDevices(roomID, apiKey):
    try:
        if(apiKey != os.getenv('API_KEY')):
            return "Unauthenticated"
        collection = db.collection('rooms')
        doc = collection.document(roomID)
        doc.update({'devices':True})
        return "done"
    except:
        return "error"

@app.route("/switchoff/<roomID>/<apiKey>")
def turnOffDevices(roomID, apiKey):
    try:
        if(apiKey != os.getenv('API_KEY')):
            return "Unauthenticated"
        collection = db.collection('rooms')
        doc = collection.document(roomID)
        doc.update({'devices':False})
        return "done"
    except:
        return "error"

@app.route("/fetchautomation/<roomID>/<apiKey>")
def fetchAutomation(roomID, apiKey):
    try:
        if(apiKey != os.getenv('API_KEY')):
            return "Unauthenticated"
        collection = db.collection('rooms')
        doc = collection.document(roomID)
        room = doc.get()
        if room.exists:
            if (room.to_dict()['automation']):
                automation = "on"
            else:
                automation = "off"
            return automation
    except:
        return "error"

if __name__ == '__main__':
    app.run()
