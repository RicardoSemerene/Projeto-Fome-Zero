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

########### Limpeza de Dados #######

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

st.sidebar.markdown('## Selecione as avaliações que pretende contemplar na análise')

rating_options = st.sidebar.multiselect(
    "Avaliação do Restaurante: (o 'X' remove todas as avaliações)",
    sorted(df1["aggregate_rating"].unique()),
    default=  sorted(df1["aggregate_rating"].unique())
)

country_options = st.sidebar.multiselect (
    
    ' Selecione os países', 
    df1["country"].unique(),
    default=  df1["country"].unique()
    )

#Filtro de Avaliações
linhas_selecionadas = df1['aggregate_rating'].isin(rating_options)
df1 = df1.loc[linhas_selecionadas,:]

#Filtro de Países
linhas_selecionadas = df1['country'].isin(country_options)
df1 = df1.loc[linhas_selecionadas,:]

######## Layout Streamlit #########
st.header('🏠 Visão Cidades')

df_aux = (df1.loc[:,['cuisines','city']].groupby('city')
                                       .nunique()
                                       .sort_values('cuisines', ascending=False)
                                       .reset_index()
                                       .head(20))

fig = px.bar(df_aux,
            x='city',
            y='cuisines', 
            color='city',
            title='Quantidades de Culinárias distintas por Cidade', 
            labels={'cuisines': 'Qtd. Culinárias','city':'Cidade'})

st.plotly_chart(fig,use_container_width = True)

with st.container():
    col1,col2 = st.columns(2)

    with col1:
        df_aux = (df1.loc[:,['city','votes']].groupby('city')
                                            .mean().sort_values('votes', ascending=False)
                                            .reset_index()
                                            .round(2)
                                            .head(6))
        fig = px.bar(df_aux, 
                     x='city',
                     y='votes', 
                     color='city',
                     labels={'votes': 'Qtd. Avaliações','city': 'Cidades'}, 
                     width=450, title='Média de Avaliações feitas por Cidade')
   
        st.plotly_chart(fig,use_container_width=True)
        
    with col2:
        df_aux = (df1.loc[df1['is_delivering_now'] == 1,
                          ['is_delivering_now','city']].groupby('city')
                                                        .count()
                                                        .sort_values('is_delivering_now', ascending=False)
                                                        .reset_index()
                                                        .head(6))
        
        fig = px.bar(df_aux, 
                        x='city',
                        y='is_delivering_now', 
                        color='city',
                        width=500,
                        labels={'city': 'Cidades','is_delivering_now': 'Qtd.Restaurantes'}, 
                        title='Cidades por Qtd. de restaurantes que fazem entregas')
    
        st.plotly_chart(fig,use_container_width=True)
        
df_aux = (df1.loc[df1['price_range'] == 4,['city','restaurant_name']].groupby('city')
                                                                    .count().sort_values('restaurant_name', ascending=False)
                                                                    .reset_index()
                                                                    .head(20))

fig = px.bar(df_aux, 
             x='city',
             y='restaurant_name', 
             color='city', 
             title='Quantidade de Restaurantes Gourmet por Cidade', 
             labels={'restaurant_name': 'Qtd. Restaurantes', 'city': 'Cidades'})

st.plotly_chart(fig,use_container_width=True)