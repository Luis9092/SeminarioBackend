import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('database/seminarioproyecto-b315e-f9b8570104d8.json')
firebase_admin.initialize_app(
            cred, {"storageBucket": "seminarioproyecto-b315e.appspot.com"}
        )

# app = firebase_admin.initialize_app(cred)

db = firestore.client()

bucket = storage.bucket()