import streamlit as st
import pyrebase
import json

def connectFirebase():
    firebaseConfig = json.loads(st.secrets["text-api-key"])
    credentials = json.loads(st.secrets["text-credentials"])
    firebaseConfig["serviceAccount"] = credentials

    firebase = pyrebase.initialize_app(firebaseConfig)
    
    auth = firebase.auth()
    db = firebase.database()
    storage = firebase.storage()

    if 'auth' not in st.session_state:
        st.session_state['auth'] = auth
    if 'db' not in st.session_state:
        st.session_state['db'] = db
    if 'storage' not in st.session_state:
        st.session_state['storage'] = storage