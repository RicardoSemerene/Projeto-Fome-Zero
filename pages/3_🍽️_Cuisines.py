#Bibliotecas
import plotly.express as px
import inflection 
import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Projeto Fome Zero',
    page_icon='logo.png',
    layout='wide'
)

# Importando Dados
df = pd.read_csv('zomato.csv')
df1 = df.copy(deep=True)

########### Funções #######

def metricas (cuisine):
    df_aux = df1.loc[(df1['cuisines'] == cuisine) & (df1['aggregate_rating'] == 4.9),['restaurant_name','aggregate_rating','restaurant_id']].sort_values('restaurant_id').reset_index().head(1)
    df_aux = df_aux.drop('index', axis=1)
    maximo_name = df_aux.loc[:,'restaurant_name'].max()
    maximo_number = df_aux.loc[:,'aggregate_rating'].max()

    return maximo_name,maximo_number

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
st.sidebar.image(image,width=50)

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('''---''')

st.sidebar.markdown('## Selecione quantos restautantes deseja analisar')

restaurant_slider = st.sidebar.slider(
    'Até quantos restautantes ?',
    value = 20, min_value = 0, max_value = 20  
)

country_options = st.sidebar.multiselect (
    
    ' Selecione os países', 
    df1["country"].unique(),
    default=  df1["country"].unique()
    )

#Filtro de Países
linhas_selecionadas = df1['country'].isin(country_options)
df1 = df1.loc[linhas_selecionadas,:]

######## Layout Streamlit #######
st.header('🍽️ Visão Tipos Culinários')
st.markdown(' ## Melhores Restaurantes dos Principais tipos Culinários')

col1,col2,col3,col4,col5 = st.columns (5)
with col1:
    maximo_name, maximo_number = metricas ('Italian')
    col1.metric("Italiana: {}".format(maximo_name),"{}/5.0".format(maximo_number))
    
with col2:
    maximo_name, maximo_number = metricas ('American')
    col2.metric("Americana: {}".format(maximo_name),"{}/5.0".format(maximo_number))
    
with col3:
    maximo_name, maximo_number = metricas ('Indian')
    col3.metric("Indiana: {}".format(maximo_name),"{}/5.0".format(maximo_number))
    
with col4:
    maximo_name, maximo_number = metricas ('Japanese')
    col4.metric("Japonesa: {}".format(maximo_name),"{}/5.0".format(maximo_number))
    
with col5:
    maximo_name, maximo_number = metricas ('Brazilian')
    col5.metric("Brasileira: {}".format(maximo_name),"{}/5.0".format(maximo_number))
    
cols = ['restaurant_id','restaurant_name','city','country','cuisines','aggregate_rating']
df2 = (df1.loc[:, cols].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])
                       .reset_index()
                       .drop('index', axis=1)
                       .head(restaurant_slider))

st.dataframe(df2,width=1400,height=900)

