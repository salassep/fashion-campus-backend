import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from dotenv import load_dotenv

def get_bucket():
    load_dotenv()

    cred = credentials.Certificate("fashion-campus-firebase-adminsdk-u6ode-45a90533e5.json")

    try:
        app = firebase_admin.initialize_app(cred, {'storageBucket': 'fashion-campus.appspot.com'}, name='storage')
        bucket = storage.bucket(app=app)
        return bucket
    except:
        app = firebase_admin.get_app(name='storage')
        bucket = storage.bucket(app=app)
        return bucket