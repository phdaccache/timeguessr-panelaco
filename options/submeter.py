import streamlit as st
from streamlit_folium import st_folium
import folium
from PIL import Image

def run_submeter():
    st.markdown("<h1 style='text-align: center; color: black; font-weight: bold;font-family: Verdana, sans-serif; font-size:35px;'>Submeta suas Fotos &#127909</h1>", unsafe_allow_html=True)

    foto = st.file_uploader("Submeter Foto:", type="jpg")

    form2 = st.form("Position entry form submeter")

    with form2:
        nome = st.text_input("Seu nome:",value="Anônimo")
        desc = st.text_area("Descrição da foto:",value="Vazio")

        c1, c2 = st.columns(2)

        with c1:
            if foto is not None:
                st.image(foto)

        with c2:
            DEFAULT_LATITUDE = 51.
            DEFAULT_LONGITUDE = 3.

            m = folium.Map(location=[DEFAULT_LATITUDE, DEFAULT_LONGITUDE], zoom_start=1)

            # The code below will be responsible for displaying 
            # the popup with the latitude and longitude shown
            m.add_child(folium.LatLngPopup())

            f_map = st_folium(m, width=400,height=300)

            ano = st.slider("Escolha uma data:", min_value=1900, max_value=2024, value=1962)

        selected_latitude = None
        selected_longitude = None

        if f_map.get("last_clicked"):
            selected_latitude = f_map["last_clicked"]["lat"]
            selected_longitude = f_map["last_clicked"]["lng"]

    submit = form2.form_submit_button("Submeter")

    if submit:
        if foto == None:
            st.warning("Escolha uma foto!")
        elif selected_latitude == None or selected_longitude == None:
            st.warning("Escolha um lugar no mapa!")
        else:
            db = st.session_state['db']
            storage = st.session_state['storage']
            user = st.session_state['user']

            foto_dic = {
                "ano": ano,
                "desc": desc,
                "lat": selected_latitude,
                "long": selected_longitude,
                "nome": nome
            }

            total_photos = db.child("Users").child(user["localId"]).child("totalfotos").get().val()
            num_foto = total_photos+1

            db.child("Users").child(user["localId"]).child("totalfotos").set(num_foto)
            db.child("Users").child(user["localId"]).child("status").update({num_foto: False})
            db.child("Users").child(user["localId"]).child("fotos").child(num_foto).set(foto_dic)

            upload_foto = Image.open(foto)
            upload_foto.save(f"{num_foto}phdaccache.jpg")
            storage.child(f"images/{num_foto}.jpg").put(f"{num_foto}phdaccache.jpg")

            st.success("Foto enviada!")

    if st.button("Voltar Página Inicial"):
        st.session_state["page_option"] = "home"
        st.rerun()