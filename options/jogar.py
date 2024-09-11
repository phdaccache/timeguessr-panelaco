import streamlit as st
from streamlit_folium import st_folium
import folium
import random
from datetime import datetime

def get_image():
    db = st.session_state['db']
    storage = st.session_state['storage']
    user = st.session_state['user']
    total_photos = db.child("Users").child(user["localId"]).child("totalfotos").get().val()
    status = db.child("Users").child(user["localId"]).child("status").get().val()
    fotodia = db.child("Users").child(user["localId"]).child("fotodia").get().val()

    current_day = list(fotodia)[0]
    today = datetime.today().strftime('%Y-%m-%d')
    if current_day == today:
        image = storage.child(f"images/{fotodia[today]}.jpg").get_url(user["idToken"])
        return image, fotodia[today]

    possible_images = []
    no_images = True
    for pos, value in enumerate(status):
        if not value:
            no_images = False
            possible_images.append(pos+1)
    
    if no_images:
        return None, 0
    
    random_num = random.randint(0, len(possible_images)-1)
    image_num = possible_images[random_num]
    fotodia = db.child("Users").child(user["localId"]).child("fotodia").remove()
    fotodia = db.child("Users").child(user["localId"]).child("fotodia").update({today:image_num})
    db.child("Users").child(user["localId"]).child("status").child(image_num).set(True)
    image = storage.child(f"images/{image_num}.jpg").get_url(user["idToken"])
    return image, image_num

def run_jogar():
    st.markdown("<h1 style='text-align: center; color: black; font-weight: bold;font-family: Verdana, sans-serif; font-size:35px;'>Adivinhe o Local &#128205 e a Data &#128198</h1>", unsafe_allow_html=True)
    
    image, num_image = get_image()
    
    form1 = st.form("Position entry form jogar")

    with form1:
        c1, c2 = st.columns(2)

        with c1:
            if image == None:
                st.warning("Não há imagens novas :(")
                no_images = True
            else:
                st.image(image)
                no_images = False

        with c2:
            DEFAULT_LATITUDE = 51.
            DEFAULT_LONGITUDE = 3.

            m = folium.Map(location=[DEFAULT_LATITUDE, DEFAULT_LONGITUDE], zoom_start=1)

            # The code below will be responsible for displaying 
            # the popup with the latitude and longitude shown
            m.add_child(folium.LatLngPopup())

            f_map = st_folium(m, width=400,height=300)

            data_escolhida = st.slider("Escolha uma data:", min_value=1900, max_value=2024, value=1962)

        selected_latitude = None
        selected_longitude = None

        if f_map.get("last_clicked"):
            selected_latitude = f_map["last_clicked"]["lat"]
            selected_longitude = f_map["last_clicked"]["lng"]

    submit = form1.form_submit_button("Adivinhar")

    if submit:
        if no_images:
            st.warning("Não há imagens!")
        elif selected_latitude == None and selected_longitude == None:
            st.warning("Escolha um lugar do mapa!")
        else:
            db = st.session_state['db']
            user = st.session_state['user']

            nome = db.child("Users").child(user["localId"]).child("fotos").child(num_image).child("nome").get().val()
            desc = db.child("Users").child(user["localId"]).child("fotos").child(num_image).child("desc").get().val()
            lat = db.child("Users").child(user["localId"]).child("fotos").child(num_image).child("lat").get().val()
            long = db.child("Users").child(user["localId"]).child("fotos").child(num_image).child("long").get().val()
            ano = db.child("Users").child(user["localId"]).child("fotos").child(num_image).child("ano").get().val()

            coords_1 = (lat, long)
            coords_2 = (selected_latitude, selected_longitude)

            st.session_state["coords_1"] = coords_1
            st.session_state["coords_2"] = coords_2
            st.session_state["data_certa"] = ano
            st.session_state["data_escolhida"] = data_escolhida
            st.session_state["nome"] = nome
            st.session_state["desc"] = desc
            st.session_state["image"] = image
            st.session_state["page_option"] = "resultado"
            st.rerun()
            
    if st.button("Voltar Página Inicial"):
        st.session_state["page_option"] = "home"
        st.rerun()