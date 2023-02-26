
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine

# Blibiotecas necessárias
import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
import folium
from streamlit_folium import folium_static

# ------------------------------------------
# Funçoes
# ------------------------------------------

def avg_std_time_delivery( df1, festival, op ):
    """esta função calcula o tempo médio e desvio padrão do tempo de entrega.
    Parametros:
         Input:
            - df: Dataframe com dadosnessessarios para calculo
            - op: tipo de operaçao que pressisa ser calculado
                'avg_time', calcula o tempo medio
                'std_time', calcula o desvio padrão do tempo.
            Output:
              - df : Dataframe com 2 colunas 1 linha.
              
    """
    df_aux = (df1.loc[:, ['Time_taken(min)', 'Festival']]
                 .groupby( 'Festival' )
                 .agg( {'Time_taken(min)': ['mean', 'std']}))
            
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index() 
    df_aux = np.round( df_aux.loc[df_aux['Festival'] == festival, op], 2 )
    return df_aux

def co2( df1 ):

        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
        df1['distance'] = ( df1.loc[:, cols]
                               .apply( lambda x:
                                      haversine(  (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                  (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis = 1) )

        avg_distance = np.round( df1['distance'].mean() )
        return avg_distance            


def t_m_d_e_p_c( df1 ):
                cols = ['City', 'Time_taken(min)' ]
                df_aux = df1.loc[:, cols].groupby('City').agg( {'Time_taken(min)': ['mean', 'std']})
                df_aux.columns = ['avg_time', 'std_time']
                df_aux = df_aux.reset_index()
                fig = go.Figure()
                fig.add_trace( go.Bar( name='Control',
                                       x=df_aux['City'],
                                       y=df_aux['avg_time'],
                                       error_y=dict( type='data', array=df_aux['std_time'])))
                fig.update_layout(barmode='group')
                return fig
            

def distribuiçao_de_distancia( df1 ):
                df_aux = ( df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']]
                              .groupby(['City', 'Type_of_order'])
                              .agg( {'Time_taken(min)': ['mean', 'std']}) )
                df_aux.columns = ['avg_time', 'std_time']
                df_aux = df_aux.reset_index()
                return df_aux

def d_d_r_r( df1 ):
                cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
                df1['distance'] = df1.loc[:, cols ].apply( lambda x:
                                                          haversine(  (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                                      (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis = 1)

                avg_distance = df1.loc[:, ['City', 'distance']].groupby( 'City' ).mean().reset_index()
                fig = go.Figure ( data=[ go.Pie( labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])
                return fig

def c_t_r( df1 ):
                cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
                df_aux = ( df1.loc[:, cols]
                             .groupby(['City', 'Road_traffic_density'])
                             .agg( {'Time_taken(min)': ['mean', 'std']}) )
                df_aux.columns = ['avg_time', 'std_time']
                df_aux = df_aux.reset_index()
                fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                                  color='std_time', color_continuous_scale='RdBu',
                                  color_continuous_midpoint=np.average(df_aux['std_time']))
                return fig

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
                       
st.header('Marktplace - Visão Restaurant') 

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
f1 = df1.loc[linhas_selecionadas, :]


#=====================================
# Layout no Streamlit
#===================================== 

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática','Visão Geográfica'] ) 

with tab1:
    with st.container():
        st.title( 'Overall Metrics' )
        col1, col2, col3, col4, col5, col6 =st.columns( 6 )
        with col1:
            df_aux = len(df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric( 'Entregadores únicos', df_aux )

        with col2:
            avg_distance = co2( df1 )
            col2.metric( 'A distancia media das entregas', avg_distance )
            
        with col3:
            df_aux = avg_std_time_delivery( df1, 'Yes', 'avg_time' )
            col3.metric( 'Tempo Médio de Entrega com festival', df_aux )      
                                     
        with col4:
            df_aux = avg_std_time_delivery( df1, 'Yes',  'std_time' )
            col4.metric( 'STD Entrega', df_aux )
                    
        with col5:
            df_aux = avg_std_time_delivery( df1, 'No', 'avg_time' )
            col5.metric( 'Tempo Médio ', df_aux )
                      
        with col6:
            df_aux = avg_std_time_delivery( df1 , 'No', 'std_time' )
            col6.metric( 'STD Entrega ', df_aux )    
        
    with st.container():
        st.markdown("""___""")
        col1, col2 = st.columns( 2 )
        
        
        with col1:
            fig = t_m_d_e_p_c( df1 )
            st.title( 'Tempo médio de Entrega por cidade' )
            st.plotly_chart( fig,use_container_width=True )

            
        with col2:
            df_aux = distribuiçao_de_distancia( df1 )
            st.title( 'Distribuição de Distancia' )
            st.dataframe ( df_aux,use_container_width=True )
            
    with st.container():
        st.markdown("""___""")
        st.title( 'Distribuicao do tempo' )
        
        col1, col2 = st.columns( 2 )
        with col1:
            fig = d_d_r_r( df1 )
            st.plotly_chart ( fig,use_container_width=True ) 
            
            
        with col2:
            fig = c_t_r( df1 )
            st.plotly_chart( fig,use_container_width=True )
            

            


































































