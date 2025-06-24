import streamlit as st
import pyrebase
import json

import options.authentication as at

def connectFirebase():
    firebaseConfig = json.loads(st.secrets["text-api-key"])
    credentials = json.loads(st.secrets["text-credentials"])
    firebaseConfig["serviceAccount"] = credentials

    firebase = pyrebase.initialize_app(firebaseConfig)
    
    auth = firebase.auth()

    user, auth_status = at.runLoginPage()

    db = firebase.database()
    storage = firebase.storage()

    if 'auth' not in st.session_state:
        st.session_state['auth'] = auth
    if 'db' not in st.session_state:
        st.session_state['db'] = db
    if 'storage' not in st.session_state:
        st.session_state['storage'] = storage

    return user, auth_status