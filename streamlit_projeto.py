# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 16:08:06 2025

@author: Diogo Chikhi
"""
import sys
import os

# Adiciona o diretório 'src' ao caminho de pesquisa de módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Agora você pode importar seus módulos normalmente
from Short_features import filter_features
from extractfilesfinal import extract

from streamlit.components.v1 import html
import time

import streamlit as st
import os
from sklearn.preprocessing import StandardScaler
from Short_features import filter_features
from SVM_Leave_one_out import modelo
import pandas as pd
import streamlit.components.v1 as components
from streamlit.runtime.scriptrunner import add_script_run_ctx
import threading as th
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from streamlit_autorefresh import st_autorefresh
import uuid

# Configurações do dispositivo BLE
DEVICE_NAME = "NEVESBP"
SERVICE_UUID = uuid.UUID("9a27ed68-4948-4029-b666-8bc9a12ab4e2")
CHAR_UUID = uuid.UUID("9a27ed68-4948-4029-b666-8bc9a12ab4e2")

# Configurações do MQTT
MQTT_BROKER = "192.168.1.98"
MQTT_PORT = 1883
MQTT_TOPIC = "AAI/NEVESBP"
START_TOPIC = "acquisition/start"
STOP_TOPIC = "acquisition/stop"

# Caminho para a imagem de fundo
image_path = r"C:\Users\Diogo Chikhi\OneDrive\Ambiente de Trabalho\Faculdade\4ano\AAI\lab6\papicris.jpg"
def add_animation(page_name, animation_type='fadeIn'):
    page_animation = f"""
    <style>
        .page-{page_name} {{
            animation: {animation_type} 2s;
        }}
        @keyframes fadeIn {{
            0% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}
        @keyframes fadeOut {{
            0% {{ opacity: 1; }}
            100% {{ opacity: 0; }}
        }}
    </style>
    """
    components.html(page_animation, height=0)


# Página principal
def main_page():
    add_animation('home', 'fadeIn')
    st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://static.vecteezy.com/ti/vetor-gratis/p1/9482455-futebol-campo-futebol-campo-fundo-vetor.jpg');
        background-size: cover;
        background-position: center;
        ackground-color: rgba(0, 0, 0, 0.5);
        height: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: black;">Football Kick Simulator</h1>
        <h2 style="color: black;">Football Learning Tool Using Machine Learning</h2>
    </div>
    """,
    unsafe_allow_html=True
)
    st.write('')
    st.write('')
    
    motivation = 'We have designed this program in order to help football players analyze and identify the type of pass they make. Using machine learning, it evaluates the mechanics of each pass, whether it is a pass with the inside of the foot, the outside or a toe poke. By providing real-time feedback, the tool helps players refine their passing technique and track their progress. This technology empowers athletes to improve their passing consistency, ultimately boosting their overall performance and contribution to the team.'
    st.markdown(
    f"""
    <div style="text-align: justify;">
        <span style="color:black">{motivation}</span>
    <div>
    """,
    unsafe_allow_html=True
)
    image_path = "https://media1.tenor.com/m/UOXzaNGSpuwAAAAd/cristiano-ronaldo.gif"
    st.write('')
    st.write('')
    st.image(image_path,width= 250, use_column_width = True)
    
    

    

    if st.button('Next'):
        add_animation('home', 'fadeOut')
        

        st.session_state.page = 'segunda_pagina'
        
# Segunda página
def segunda_pagina():
    
    
    st.markdown(
    """
    <div class="slide-in">
    <style>
    .stApp {
        background-image: url('https://static.vecteezy.com/ti/vetor-gratis/p1/9482455-futebol-campo-futebol-campo-fundo-vetor.jpg');
        background-size: cover;
        background-position: center;
        height: 100%;
    } 
    </style>
    """,
    unsafe_allow_html=True
)
    def MQTT_TH(client):

        # MQTT Callbacks
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+str(rc))
            client.subscribe(st.session_state['MyData']['TopicSub'])  # Subscribe to the topic for receiving the file
        
        def on_message(client, userdata, msg):
            print(msg.topic+" "+str(msg.payload))
        
        # Diretório onde o ficheiro será salvo
            save_directory = r"C:\Users\Diogo Chikhi\OneDrive\Ambiente de Trabalho\Faculdade\4ano\AAI\lab6\dado de teste"
            os.makedirs(save_directory, exist_ok=True)  # Certifica-se de que o diretório existe

            file_path = os.path.join(save_directory, "received_file.txt")  # Caminho completo do ficheiro
        
            try:
            # Salvar o conteúdo do ficheiro como texto
                with open(file_path, "w") as f:
                    f.write(msg.payload.decode("utf-8"))  # Convertendo bytes para string
                st.session_state['MyData']['Message'] = f"File saved at {file_path}"
            except Exception as e:
                st.session_state['MyData']['Message'] = f"Error saving file: {e}"

        print('Initializing MQTT')
        client.on_connect = on_connect
        client.on_message = on_message
        st.session_state['MyData']['Run'] = True
        client.connect(st.session_state['MyData']['Broker'], 1883, 60)
        client.loop_forever()  # Keep the MQTT client listening for messages
        print('MQTT link ended')
        st.session_state['MyData']['Run'] = False


    # Stores states of variables between page refresh
    if 'MyData' not in st.session_state:
        st.session_state['MyData'] = {'Run': False, 'Broker':'192.168.1.98', 'TopicSub':'AAI/NEVESBP',
                                      'Topic':'', 'Message':''}

    # MQTT session information
    if 'mqttThread' not in st.session_state:
        st.session_state.mqttClient = mqtt.Client()
        st.session_state.mqttThread = th.Thread(target=MQTT_TH, args=[st.session_state.mqttClient]) 
        add_script_run_ctx(st.session_state.mqttThread)

    #### Page design starts here
    st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: black;">MQTT Communication</h1>
        
    </div>
    
    
    """,
    unsafe_allow_html=True
)
   

    # MQTT configuration
    st.session_state['MyData']['Broker'] = st.text_input('MQTT Broker: ', value='192.168.1.98')
    st.session_state['MyData']['TopicSub'] = st.text_input('Topic subscribed: ', value='AAI/NEVESBP')  # Topic where the file is published
    col4, col5, col6,col7,col8 = st.columns([1,1,1,1, 1])  # Divide novamente para centralizar
    with col6:
        if st.session_state['MyData']['Run']:
            if st.button('MQTT disconnect'):
                st.session_state.mqttClient.disconnect()
        else:
            if st.button('MQTT connect'):
                st.session_state.mqttThread.start()  # Starts thread that controls MQTT
    st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: black;">Acquisition Control</h1>
        
    </div>
    
    
    """,
    unsafe_allow_html=True
)
    st.write('')
    st.write('')
    st.write('')
    col1, col2, col3,col4 , col5  =st.columns([1,2,1,2,1])    
    
    # Interface do Streamlit
    with col2:
        if st.button("Start acquisition"):
            publish.single(START_TOPIC, payload="start", hostname=MQTT_BROKER)
            st.success("Comando enviado: Iniciar Aquisição")
    with col4:    
        if st.button("Stop acquisition"):
            publish.single(STOP_TOPIC, payload="stop", hostname=MQTT_BROKER)
            st.warning("Comando enviado: Parar Aquisição")

    st_autorefresh(interval=1000, key="fizzbuzzcounter")

    # MQTT Thread Function
    

    # Display messages received in subscribed topic
    st.markdown(
    """
    <div style="text-align: center;">
        <h2 style="color: black;">Messages Received</h2>
        
    </div>
    
    
    """,
    unsafe_allow_html=True
)
    
    st.text('Topic: ' + st.session_state['MyData']['Topic'])
    st.text('Message: ' + st.session_state['MyData']['Message'])

    # After receiving a file
    if st.session_state['MyData']['Message'] == "File saved as 'received_file.txt'":
        st.success("File received and saved as 'received_file.txt'.")

    # Error messages if the file decoding fails
    if "Error decoding file" in st.session_state['MyData']['Message']:
        st.error(st.session_state['MyData']['Message'])

    # Função para processar os dados e fazer previsões
    def process_and_predict(samples_path):
        # Extrair e filtrar as features
        dfn = filter_features(samples_path)

        # Separar features (X) e rótulos (se aplicável)
        Xn = dfn.drop(columns=['File', 'Class'], errors='ignore')

        # Normalizar os dados
        scaler = StandardScaler()
        #new_samples_scaled = scaler.fit_transform(Xn)

        # Fazer previsões usando o modelo previamente treinado
        new_predictions = modelo.predict(Xn)
        

        # Criar um DataFrame com os resultados
        results = pd.DataFrame({
            'Sample': dfn['File'] if 'File' in dfn.columns else range(1, len(new_predictions) + 1),
            'Predicted Class': new_predictions
        })
        results.index = pd.RangeIndex(start=1, stop=len(results) + 1, step=1)
        return results

    # Configurar a interface do Streamlit
    st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: black;">Movement Predicted:</h1>
        
    </div>
    
    
    """,
    unsafe_allow_html=True
)   
    st.write('')
    st.write('')
    st.write('')
  
    # Selecionar o diretório com os dados
    samples_path = r"C:\Users\Diogo Chikhi\OneDrive\Ambiente de Trabalho\Faculdade\4ano\AAI\lab6\dados de teste"

    

# Certifique-se de que as imagens estão no mesmo diretório ou em um caminho acessível
   
    

    col9, col10, col11, col12, col13 = st.columns([1, 1, 1, 1, 1])  # Divide novamente para centralizar
    with col11:  # Botão para processar os dados e exibir os resultados
        if st.button("Process and Predict"):
            if os.path.isdir(samples_path):
                try:
                    results = process_and_predict(samples_path)
                    st.session_state['results'] = results  # Armazena os resultados na sessão
                    st.success("Successfully Predicted!")
                except Exception as e:
                    st.session_state['results'] = None  # Reseta os resultados em caso de erro
                    st.error(f"Error processing data: {e}")
            else:
                st.error("Incorrect Path")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

# Exibe os resultados armazenados, se existirem
    
    col14, col15, col16 = st.columns([2, 1, 1])
    # Exibe os resultados armazenados, se existirem
    
    if "results" in st.session_state and st.session_state["results"] is not None:
        with col14:
            st.dataframe(st.session_state["results"])

        # Cria botões para cada linha da tabela
        for index, row in st.session_state["results"].iterrows():
            resultado = row["Predicted Class"]
            with col16:
                if st.button(f"Visualizar Resultado {index}", key=f"button_{index}"):
                    st.session_state.selected_index = index-1
                    st.session_state.page = "resultado_pagina"

    # Botão para voltar ao início
    if st.button("Voltar para Página Inicial"):
        st.session_state.page = "main_page"
#testes começão aqui 
def resultado_pagina():
    st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://static.vecteezy.com/ti/vetor-gratis/p1/9482455-futebol-campo-futebol-campo-fundo-vetor.jpg');
        background-size: cover;
        background-position: center;
        height: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    IMAGE_PATHS = {
        "trivela": ["https://media.tenor.com/5a_1scoQzRAAAAAM/a12.gif","https://media1.tenor.com/m/TIYtFGsgs9YAAAAd/cancelo-sterling.gif"],  # Substitua pelo caminho real
        "biqueira": ["C:/Users/Diogo Chikhi/OneDrive/Ambiente de Trabalho/Faculdade/4ano/AAI/lab6/imagens_projeto/futsal.jpg"],  # Substitua pelo caminho real
        "parte de dentro":[ 'https://media1.tenor.com/m/ec8FqQq4WioAAAAd/ronaldo-vs-barcelona-ronaldo-goal.gif',  # Substitua pelo caminho real'
        "https://media1.tenor.com/m/b11exRjzmDgAAAAd/kdb-pass.gif"],
        "rejeicao": [ "C:/Users/Diogo Chikhi/OneDrive/Ambiente de Trabalho/Faculdade/4ano/AAI/lab6/imagens_projeto/rejeicao.jpg"]
}
    CONTENT = {
    "trivela": [
        "A trivela é um tipo de passe ou chute realizado com o lado externo do pé.",
        "Este movimento é caracterizado por seu efeito curvado."
    ],
    "biqueira": [
        "A biqueira é usada em chutes de emergência para máxima força.",
        "Frequentemente utilizada no futsal."
    ],
    "parte de dentro":["A parte de dentro do pé é a parte mais usada quer no futebol quer no futsal. Eis alguns exemplos do tipo de chute/passe que podes efetuar:",'Shooting or passing with the inside of the foot is a technique that prioritizes accuracy and control, making it ideal for precise ball distribution or strikes. When using the inside of the foot, the larger surface area provides a stable, controlled connection with the ball, resulting in a straighter and more predictable trajectory. This technique also allows for the generation of topspin or sidespin, which can help curve the ball around defenders or make it dip during a shot. It is especially useful for short and medium passes in tight spaces, as it offers greater precision in quick, tactical plays. Additionally, it is commonly used for crossing the ball into dangerous areas or shooting in tight situations, where aiming for the far post or a precise location is essential. Overall, the inside of the foot is a versatile tool that helps players maintain control and accuracy, particularly when power is not the main focus.'],
    
    "rejeicao":["You're just a chill guy who didn't do any movement"]
}
    AUDIOS={
        "trivela":'',
        "biqueira":'',
        "parte de dentro":'',
        "rejeicao":"C:/Users/Diogo Chikhi/OneDrive/Ambiente de Trabalho/Faculdade/4ano/AAI/chill-guy.mp3"
        }

    # Verifica se o índice foi definido no estado da sessão
    if "selected_index" in st.session_state and "results" in st.session_state:
        selected_index = st.session_state["selected_index"]
        selected_row = st.session_state["results"].iloc[selected_index]
        resultado = selected_row["Predicted Class"]
        imagem = IMAGE_PATHS.get(resultado,[])
        textos = CONTENT.get(resultado, [])
        audio=AUDIOS.get(resultado)# Exibe a imagem e o resultado
        st.markdown(
            """
            <div style="text-align: center;">
               <h1 style="color: black;">Detalhes do Resultado</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
       

        if textos:
            st.markdown(
               f"""
               
               <h2 style="color:black">Classe prevista: {resultado}</h2>
               <p></p>
               
               """,
                unsafe_allow_html=True
       )
            for texto in textos:
                
                
                st.markdown(
                   f"""
                  
                   <span style="color:black">{texto}</span>
                   """,
                    unsafe_allow_html=True
           )
        else:
            st.write("Nenhum texto disponível para este resultado.")
        if imagem:
    # Dividir o layout em colunas, ajustando o número conforme necessário
            cols = st.columns(len(imagem))

    # Exibir cada imagem em uma coluna
            for col, img in zip(cols, imagem):
                with col:
                   st.image(img, use_column_width=True)  # Use use_column_width para ajuste automático
        else:
            st.write("Nenhum texto disponível para este resultado.")
       
        if audio == '':
            st.write('')
        else:
            
            st.audio(audio,format='audio/mp3', start_time=0) 
    # Botão para voltar à página principal
    if st.button("Voltar para Resultados"):
        st.session_state.page = "segunda_pagina"



# Verificando qual página exibir
if 'page' not in st.session_state:
    st.session_state.page = 'main_page'

if st.session_state.page == 'main_page':
    main_page()
elif st.session_state.page == 'segunda_pagina':
    segunda_pagina()
elif st.session_state.page == "resultado_pagina":
    resultado_pagina()

