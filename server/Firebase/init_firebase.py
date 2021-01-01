import firebase_admin
from firebase_admin import credentials, firestore
from Firebase.fb_utils import get_full_path

path = get_full_path('cfg/Minion_key.json')
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)

db = firestore.client()
