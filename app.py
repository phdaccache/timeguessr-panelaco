import streamlit as st
from firebase_connection.firebase import connectFirebase
import options.authentication as at
import options.home as hm
import options.jogar as jg
import options.resultado as rt
import options.submeter as sb

# App
st.set_page_config(
     page_title = "Timeguessr Panelaço",
)

# Getting authentication and database modules from Firebase
# Puts auth and db on st.session_state
connectFirebase()

# Authenticating User
user, auth_status = at.runLoginPage()

# Running page if user is correctly authenticated
if auth_status == True:
    if "page_option" not in st.session_state:
        st.session_state["page_option"] = "home"

    if st.session_state["page_option"] == "home":
        hm.run_home()
    elif st.session_state["page_option"] == "jogar":
        jg.run_jogar()
    elif st.session_state["page_option"] == "submeter":
        sb.run_submeter()
    elif st.session_state["page_option"] == "resultado":
        rt.run_resultado()

# Excepting warnings/errors
col1, col2, col3 = st.columns(3)
with col2:
    if auth_status == False:
        st.error('Username/password is incorrect')
    elif auth_status == None:
        st.warning('Please enter your username and password')