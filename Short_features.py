# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 18:00:19 2024

@author: 35193
"""
from extractfilesfinal import extract
import pandas as pd



def filter_features(path):
    
   
    output_path = 'filtered_features.csv'
    
    # Carregar o arquivo CSV  
    df = extract(path)

    # Selecionar apenas a coluna File e as 5 colunas desejadas
    selected_columns = ['File', 
                        'Gyro_Z_Area under the curve', 
                        'Gyro_X_Slope', 
                        'Gyro_X_Sum absolute diff', 
                        'Gyro_X_Signal distance', 
                        'Accel_Z_Mean',
                        'Class']

    # Verificar se as colunas existem no DataFrame
    available_columns = [col for col in selected_columns if col in df.columns]
    if len(available_columns) < len(selected_columns):
        print("Aviso: Algumas colunas não foram encontradas no arquivo CSV!")

    # Filtrar o DataFrame apenas com as colunas desejadas
    filtered_df = df[available_columns]


    # Salvar o novo DataFrame em um arquivo CSV
    filtered_df.to_csv(output_path, index=False, sep=';')

    print(f"Arquivo modificado salvo em: {output_path}")
    return filtered_df

directory = r"C:\Users\Diogo Chikhi\OneDrive\Ambiente de Trabalho\Faculdade\4ano\AAI\lab6\dados"
filter_features(directory)