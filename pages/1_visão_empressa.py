# Libralis

import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine

# Blibiotecas necessárias
import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

# ------------------------------------------
# Funçoes
# ------------------------------------------

def order_metric( df1 ):
                """ esta funçao e para agrupar e e plotar grafico sobre pedidos por dia
    
                Input: Dataframe
                Output: Dataframe
                """
                # selecao de linhas e colunas
                df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby(['Order_Date']).count().reset_index()

                # desenhar o graficode linhas
                fig = px.bar(df_aux, x='Order_Date', y='ID')    

                return fig
def traffic_order_share( df1 ):
                """ esta funçao e para agrupar e e plotar grafico Compartilhamento de Ordem de Tráfego
    
                Input: Dataframe
                Output: Dataframe
                """
                df_aux = ( df1.loc[:, ['Road_traffic_density', 'ID']].groupby(['Road_traffic_density']).count().reset_index() )
                #df_aux['entregas_percent'] = df_aux['ID'] / df_aux['ID'].sum()
                fig = px.pie(df_aux, values='ID', names='Road_traffic_density')

                return fig  

def trafic_order_city( df1):
                """ esta funçao e para agrupar e e plotar grafico Cidade da Ordem de Trânsito
    
                Input: Dataframe
                Output: Dataframe
                """
                df_aux = df1.loc[:, ['Road_traffic_density', 'City', 'ID']].groupby(['Road_traffic_density', 'City']).count().reset_index()
                fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
                return fig
            
def order_by_week( df1 ):
            """ esta funçao e para agrupar e e plotar grafico ordernar por semana
    
            Input: Dataframe
            Output: Dataframe
            """
            # criando coluna de semana
            df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U' )
            df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
            fig = px.line(df_aux, x='week_of_year', y='ID')
            return fig

def order_share_by_week( df1):
            """ esta funçao e para agrupar e e plotar grafico Ordenar Partilha por Semana
    
            Input: Dataframe
            Output: Dataframe
            """
            #quantidade de pedidos por semana/Números único entrgadores por semana
            df_aux01 = df1.loc[:,['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
            df_aux02 = df1.loc[:,['Delivery_person_ID','week_of_year']].groupby( 'week_of_year' ).nunique().reset_index()

            df_aux = pd.merge( df_aux01, df_aux02, how='inner', on='week_of_year')
            df_aux['Order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

            fig = px.line( df_aux, x='week_of_year', y='Order_by_deliver')
            
            return fig 
        
def contry_maps( df1 ):
        """ esta funçao e para agrupar e e plotar mapa com os paises
    
        Input: Dataframe
        Output: Dataframe
        """
        df_aux = df1.loc[:, ['Road_traffic_density', 'City', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['Road_traffic_density', 'City']).median().reset_index()

        map = folium.Map()

        for index, location_info in df_aux.iterrows():
          folium.Marker([location_info['Delivery_location_latitude'],location_info['Delivery_location_longitude']], popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
        folium_static( map, width=1200, height=600 )

def clean_code( df1 ):
    """ Esta funcao tem a responsabilidade de limpar o dataframe 
    
        Tipos de limpesa:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços das variável de texto
        4. Formatação da coluna de datas
        5. Limpesa da coluna de tempo( remoção do texto da variável numéria )
        
        Input: Dataframe
        Output: Dataframe
    """
    #1. converter a coluna 'Age' de texto para numero
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()                       

    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()                       

    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()                       

    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )                      

    #2.convertendo a coluna 'Ratings' de texto para decimal(float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

    #3. convertendo a coluna 'Ordem_date' de texto para data                       
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')

    #4. convertendo multiple_deliveries de texto para numero inteiro(int)                      
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')                       
    df1 = df1.loc[linhas_selecionadas, :].copy()                       
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

    ##5. Removendo os espacos dentro de string/texto/object
    df1.loc[:, 'ID'] = df1.loc[0:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[0:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[0:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[0:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[0:, 'Festival'].str.strip()
    df1.loc[:, 'City'] = df1.loc[0:, 'City'].str.strip()                      

    #7. limpando a coluna de time taken                       
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply ( lambda x: x.split( '(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )
    
    return df1

# ------------------- INICIO DA ESTRUTURA LÓGICA DO CODIGO -----------------------------------
# ---------------
# Import dataset
# ---------------
df = pd.read_csv('datasets/train.csv')
df1 = df

# --------------
# Limpando dados
#---------------
df1 = clean_code( df1 )

#=====================================
# Barra Lateral
#=====================================
                       
st.header('Marktplace - Visão Cliente') 

image_path = 'image.jpg'
image = Image.open( image_path)
st.sidebar.image( image, width=120 )

st.sidebar.markdown('# Cury Company  ')                     
st.sidebar.markdown('## Fastest Delivery in Town')                       
st.sidebar.markdown("""---""")   
st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.datetime( 2022, 4, 13 ),
    min_value=pd.datetime( 2022, 2, 11 ),
    max_value=pd.datetime( 2022, 6, 4),
    format='DD-MM-YYYY'  )

                       
st.sidebar.markdown("""---""")                       
                       
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#=====================================
# Layout no Streamlit
#=====================================    
    
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática','Visão Geográfica'] )   

with tab1:
    with st.container():
        fig = order_metric( df1 )
        # Order Metric
        st.markdown( '# Orders by Day' )
        st.plotly_chart(fig,use_conteiner_width=True)
    
    with st.container():
        
        col1, col2 = st.columns(2)
        with col1:
            fig = traffic_order_share( df1 )
            st.header('Traffic Order Share')
            st.plotly_chart( fig,use_container_width=True )

        
        with col2:
            fig = trafic_order_city( df1 )
            st.header('Traffic Order City')
            st.plotly_chart( fig,use_container_width=True ) 
   
with tab2:
    with st.container():
        fig = order_by_week( df1 )
        st.markdown('# Order by Week')
        st.plotly_chart( fig,use_container_width=True )
      
        
    with st.container():
        fig = order_share_by_week( df1 )
        st.markdown('## Order Share by Week')
        st.plotly_chart( fig,use_container_width=True ) 
       
    
with tab3:
    st.markdown('# Contry Maps')
    contry_maps( df1 )
     

    
                       
                       
                       
                       