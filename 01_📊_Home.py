# Bibliotecas
import streamlit as st
from PIL import Image
import plotly.express as px 
import inflection
import pandas as pd
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster

st.set_page_config(
    page_title='Projeto Fome Zero',
    page_icon='logo.png',
    layout='wide'
)

# Importando Dados
df = pd.read_csv('zomato.csv')
df1 = df.copy(deep=True)

########### Funções #########

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    
    return df

def create_map(df):
    fig = folium.Figure(width=1920, height=1280)
    map_folium = folium.Map(max_bounds=True).add_to(fig)
    marker_cluster = MarkerCluster().add_to(map_folium)

    for _, line in df.iterrows():

        name = line["restaurant_name"]
        price_for_two = line["average_cost_for_two"]
        cuisine = line["cuisines"]
        currency = line["currency"]
        rating = line["aggregate_rating"]
        color = f'{line["rating_color"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home"),
        ).add_to(marker_cluster)

    folium_static(map_folium, width=1024, height=500)
    
########### Limpeza de Dados #######
df1 = rename_columns(df1)

df1["cuisines"] = df1["cuisines"].astype( str )
df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

countries = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

colors = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

df1["country_code"] = df1["country_code"].map(countries)
df1 = df1.rename({'country_code': 'country'}, axis = 1)
df1["rating_color"] = df1["rating_color"].map(colors)

df1 = df1.drop_duplicates()

#==========================================#
# =============BARRA LATERAL===============
#==========================================#

image = Image.open('logo.png')
st.sidebar.image(image,width=80)

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('''---''')

st.sidebar.markdown('## Selecione as avaliações que pretende contemplar na análise')

country_options = st.sidebar.multiselect (
    
    ' Selecione os países', 
    df1["country"].unique(),
    default=  df1["country"].unique()
    )

#Filtro de Países
linhas_selecionadas = df1['country'].isin(country_options)
df1 = df1.loc[linhas_selecionadas,:]

######## Layout Streamlit #########
st.header('📊 Fome Zero')
st.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')

df_aux = df1.loc[df1["country"].isin(country_options), :]
create_map(df_aux)