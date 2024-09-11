import streamlit as st
from streamlit_folium import st_folium
import folium

def run_home():
    for i in range(6):
        st.write("")
    st.markdown("<h1 style='padding: 0px;text-align: center; color: #db5049; font-family: fantasy; font-size:100px;'>TIMEGUESSR</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black; font-weight: bold;font-family: Verdana, sans-serif; font-size:35px;'>Edição Panelaço &#129368</h1>", unsafe_allow_html=True)

    st.write("")
    c1, c2, c3, c4, c5 = st.columns([2,4,4,4,1.5])
    jogar = c2.button("Jogar")
    submeter = c4.button("Submeter foto")
    
    if jogar:
        st.session_state["page_option"] = "jogar"
        st.rerun()
    elif submeter:
        st.session_state["page_option"] = "submeter"
        st.rerun()

    DEFAULT_LATITUDE = 51.
    DEFAULT_LONGITUDE = 3.
    m = folium.Map(location=[DEFAULT_LATITUDE, DEFAULT_LONGITUDE], zoom_start=1)
    st_folium(m, width=0,height=0)