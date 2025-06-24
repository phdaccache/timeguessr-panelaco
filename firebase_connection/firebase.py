import streamlit as st
import pyrebase
import json
import requests
from urllib.parse import quote
from io import BytesIO

import options.authentication as at

def connectFirebase():
    firebaseConfig = json.loads(st.secrets["text-api-key"])
    credentials = json.loads(st.secrets["text-credentials"])
    # firebaseConfig["serviceAccount"] = credentials

    firebase = pyrebase.initialize_app(firebaseConfig)
    
    auth = firebase.auth()

    if 'auth' not in st.session_state:
        st.session_state['auth'] = auth

    at.runLoginPage()

    db = firebase.database()
    storage = firebase.storage()

    if 'db' not in st.session_state:
        st.session_state['db'] = db
    if 'storage' not in st.session_state:
        st.session_state['storage'] = storage

def get_storage(path):
    user = st.session_state['user']

    encoded_path = quote(path, safe='')
    url = f"https://firebasestorage.googleapis.com/v0/b/timeguessr-panelaco.appspot.com/o/{encoded_path}?alt=media"

    headers = {
        "Authorization": f"Bearer {user['idToken']}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        print(f"Error {response.status_code}: Failed to get {path}")
        return None