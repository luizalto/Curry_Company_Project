import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Home",
    page_icon='📰'
)

image_path = 'Users/luiza/OneDrive/Documentos/blackup' 

image = Image.open( 'image.jpg' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown('# Cury Company  ')                     
st.sidebar.markdown('## Fastest Delivery in Town')                       
st.sidebar.markdown("""---""") 

st.write( '# Curry Company Growth Dashboard' )

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes. ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicado res semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Ent regador: 
        - Acompanhamento dos indicado res semanais de crescimento 
    - Visão Restaurante: 
        - Indicado res semanais de crescimento dos estaurantes 
    ### Ask for Help
    - Time de Data Science no Discord 
        - @meigarom
        
""")










