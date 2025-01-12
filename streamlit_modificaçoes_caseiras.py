# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 16:08:06 2025

@author: Diogo Chikhi
"""
# -*- coding: utf-8 -*-
"""
Updated Streamlit script for production

@author: Diogo Chikhi
"""
import os
import uuid
import tempfile
import threading as th
import pandas as pd
from sklearn.preprocessing import StandardScaler
from Short_features import filter_features
from SVM_Leave_one_out import modelo
import streamlit as st
from streamlit.components.v1 import components
from streamlit_autorefresh import st_autorefresh
from paho.mqtt.client import Client as MQTTClient
from paho.mqtt.publish import single as mqtt_publish

# MQTT Configurations
MQTT_BROKER = os.getenv("MQTT_BROKER", "127.0.0.1")  # Default to localhost
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
START_TOPIC = "acquisition/start"
STOP_TOPIC = "acquisition/stop"
DATA_TOPIC = os.getenv("DATA_TOPIC", "AAI/NEVESBP")

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_PATH = os.getenv("SAMPLES_PATH", os.path.join(BASE_DIR, "samples"))
SAVE_DIRECTORY = os.getenv("SAVE_DIRECTORY", os.path.join(BASE_DIR, "results"))
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

# Main Streamlit App
def main_page():
    st.title("Football Kick Simulator")
    st.markdown("An ML-powered tool to analyze football movements.")

    if st.button("Next"):
        st.session_state.page = 'data_acquisition'

def data_acquisition_page():
    st.title("Data Acquisition")

    st.write("### MQTT Configuration")
    broker = st.text_input("Broker", value=MQTT_BROKER)
    topic = st.text_input("Topic", value=DATA_TOPIC)

    if st.button("Connect MQTT"):
        client = MQTTClient()
        client.connect(broker, MQTT_PORT)
        st.success("Connected to MQTT broker")

    if st.button("Start Acquisition"):
        mqtt_publish(START_TOPIC, payload="start", hostname=broker)
        st.success("Acquisition started")

    if st.button("Stop Acquisition"):
        mqtt_publish(STOP_TOPIC, payload="stop", hostname=broker)
        st.warning("Acquisition stopped")
    col9, col10, col11, col12, col13 = st.columns([1, 1, 1, 1, 1])  # Divide novamente para centralizar
    with col11:  # Botão para processar os dados e exibir os resultados
        if st.button("Process and Predict"):
            if os.path.isdir(SAMPLES_PATH):
                try:
                    results = process_and_predict(SAMPLES_PATH)
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
def results_page():
    st.title("Results")

    if st.button("Process and Predict"):
        if os.path.isdir(SAMPLES_PATH):
            try:
                results = process_and_predict(SAMPLES_PATH)
                st.dataframe(results)
            except Exception as e:
                st.error(f"Error processing data: {e}")
        else:
            st.error("Samples path is invalid")

def process_and_predict(path):
    dfn = filter_features(path)
    Xn = dfn.drop(columns=['File', 'Class'], errors='ignore')
    predictions = modelo.predict(Xn)

    results = pd.DataFrame({
        'Sample': dfn['File'] if 'File' in dfn.columns else range(1, len(predictions) + 1),
        'Predicted Class': predictions
    })
    return results

# Navigation
if 'page' not in st.session_state:
    st.session_state.page = 'main_page'

if st.session_state.page == 'main_page':
    main_page()
elif st.session_state.page == 'data_acquisition':
    data_acquisition_page()
elif st.session_state.page == 'results':
    results_page()


