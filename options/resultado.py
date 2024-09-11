import streamlit as st
from streamlit_folium import st_folium
import folium
import geopy.distance
import math
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from datetime import datetime

weird_dic = {
    0: 5000,
    1: 4950,
    2: 4800,
    3: 4600,
    4: 4300,
    5: 3900,
    6: 3400,
    7: 3400,
    8: 2500,
    9: 2500,
    10: 2500,
    11: 2000,
    12: 2000,
    13: 2000,
    14: 2000,
    15: 2000,
    16: 1000,
    17: 1000,
    18: 1000,
    19: 1000,
    20: 1000
}

def share_result_image(score, years, dist, image, bg_color=(234, 232, 221)):
    response = requests.get(image)
    image = Image.open(BytesIO(response.content))
    img_size = (210, 210)
    image = image.resize(img_size)

    final_size = (1080, 1080)
    final_image = Image.open("base.png")

    center_x = (final_size[0] - img_size[0]) // 2

    # Paste the base image in the center of the final image
    Image.Image.paste(final_image, image, (center_x, 828))
    # Create drawing object
    draw = ImageDraw.Draw(final_image)


    font1 = ImageFont.load_default(40)
    font2 = ImageFont.load_default(40)

    # Prepare the text
    yt = "ano" if years == 1 else "anos"
    score_text = f"{str(score).zfill(4)}/10000"
    year_text = f"{years} {yt}"
    dist_text = dist

    # Draw text on the image
    draw.text((921, 486), score_text, font=font1, fill=(255, 255, 255, 255), align="center",anchor="md")
    draw.text((921, 608), year_text, font=font2, fill=(255, 255, 255, 255), align="center",anchor="md")
    draw.text((921, 730), dist_text, font=font2, fill=(255, 255, 255, 255), align="center",anchor="md")

    return final_image

def run_resultado():
    st.markdown("<h1 style='text-align: center; color: black; font-weight: bold;font-family: Verdana, sans-serif; font-size:35px;'>Resultado &#128203</h1>", unsafe_allow_html=True)

    coords_1 = st.session_state["coords_1"]
    coords_2 = st.session_state["coords_2"]
    data_certa = st.session_state["data_certa"]
    data_escolhida = st.session_state["data_escolhida"]
    nome = st.session_state["nome"]
    desc = st.session_state["desc"]
    image = st.session_state["image"]

    st.code(f"Foto de {nome}\nDescrição: {desc}")

    diff = abs(data_certa - data_escolhida)
    dist = geopy.distance.geodesic(coords_1, coords_2)

    c1, c2, c3 = st.columns([5,1,5])

    with c1:
        m = folium.Map(location=coords_1, zoom_start=1)
        tooltip = "Local da Foto"
        folium.Marker(
            coords_1, popup="Local da Foto", tooltip=tooltip
        ).add_to(m)
        tooltip = "Local Escolhido"
        folium.Marker(
            coords_2, popup="Local Escolhido", tooltip=tooltip
        ).add_to(m)

        f_map = st_folium(m, width=400,height=300)

        dist_score = 5000 * (math.e ** (-10 * (dist.meters)/14916862))
        dist_score = round(dist_score)
    
    with c3:
        if dist < 1:
            format_dist = dist * 1000
            format_dist = "{:.1f} m".format(format_dist.km)
        else:
            format_dist = "{:.1f} km".format(dist.km)

        if diff <= 20:
            time_score = weird_dic[diff]
        else:
            time_score = 0
        st.write(f"Distância: {format_dist}")
        st.write(f"Data certa: {str(data_certa)} - Data Escolhida: {str(data_escolhida)}")
        if diff == 0:
            st.write("Você acertou exatamente a data da foto!")
        elif diff == 1:
            st.write("Você errou por " + str(diff) + " ano!")
        else:
            st.write("Você errou por " + str(diff) + " anos!")

        for i in range(6):
            st.write("")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<h1 style='text-align: left; color: black; font-weight: bold;font-family: Verdana, sans-serif; font-size:15px;'>ANO</h1>", unsafe_allow_html=True)
            st.write(f"{time_score} / 5000")
        with col2:
            st.markdown("<h1 style='text-align: left; color: black; font-weight: bold;font-family: Verdana, sans-serif; font-size:15px;'>LOCAL</h1>", unsafe_allow_html=True)
            st.write(f"{dist_score} / 5000")
        with col3:
            st.markdown("<h1 style='text-align: left; color: black; font-weight: bold;font-family: Verdana, sans-serif; font-size:15px;'>TOTAL</h1>", unsafe_allow_html=True)
            st.write(f"{time_score+dist_score} / 10000")

    share_image = share_result_image(time_score+dist_score,diff,format_dist,image)
    data = BytesIO()
    share_image.save(data, format="PNG")
    file = data.getvalue()
    
    file_name = f"timeguessr-panelaco-{datetime.today().strftime('%Y-%m-%d')}.png"
    st.download_button("Compartilhar resultado", data=file,file_name=file_name,mime="image/png")

    if st.button("Voltar Página Inicial"):
        st.session_state["page_option"] = "home"
        st.rerun()
