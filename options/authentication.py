# External libraries
import streamlit as st

# Displays Login Page and authenticates User with auth from Firebase
def runLoginPage():
    auth, db = st.session_state['auth'], st.session_state['db']

    # Setting user status to None by default
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    if 'auth_status' not in st.session_state:
        st.session_state['auth_status'] = None

    # Little work around to rerun the app after Login so the login page disappears
    st.session_state['rerun'] = False

    # If auth_status is True, we don't want to show the Login Page again
    if st.session_state['auth_status'] != True:
        col1, col2, col3 = st.columns(3)
        with col2:
            st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)

            with st.form("Login input"):
                username = st.text_input("Username", placeholder = "Username", autocomplete="username", label_visibility="hidden")
                password = st.text_input("Password", placeholder = "Password", type = "password", autocomplete="current-password",label_visibility="hidden")
                
                submit = st.form_submit_button("Login")

                # Authenticating User
                if submit:
                    if username == "" or password == "":
                        st.session_state['auth_status'] = None
                        return st.session_state['user'], st.session_state['auth_status']
                    try:
                        email = username + "@gmail.com"
                        user = auth.sign_in_with_email_and_password(email, password)

                        st.session_state['user'] = user
                        st.session_state['auth_status'] = True
                        st.session_state['rerun'] = True
                    except:
                        st.session_state['auth_status'] = False
                        pass

    if st.session_state['rerun']:
        st.rerun()

    return st.session_state['user'], st.session_state['auth_status']