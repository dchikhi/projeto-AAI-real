# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 15:29:11 2024

@author: 35193
"""

import pandas as pd
import tsfel
import re
import os

# Diretoria com os ficheiros
directory = r"C:\Users\Diogo Chikhi\OneDrive\Ambiente de Trabalho\Faculdade\4ano\AAI\lab6\dados"  # Substitua pelo caminho da sua diretoria


def extract(path):
    
    # Listar todos os ficheiros na diretoria que terminam com ".txt"
    file_list = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".txt")]
    
    ############################### USAR PARA NOVOS DADOS ######################
    #transformed_list = []
    #for file in file_list:
        #transformed_file = transformar_ficheiro(file)
       # transformed_list.append(transformed_file)
#################################################################################

    # Initialize a list to hold the extracted features from all files
    all_features = []

    # Sampling frequency in Hz
    fs = 10  # 100 ms intervals

    for file in file_list:
        # Initialize lists to store parsed data
        time, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = [], [], [], [], [], [], []

        # Step 1: Parse each file into a DataFrame
        with open(file, "r") as f:
            for line in f:
                # Match acceleration values
                acc_match = re.search(r"Acc:\s*(-?\d+\.\d+),\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)", line)
                if acc_match:
                    accel_x.append(float(acc_match.group(1)))
                    accel_y.append(float(acc_match.group(2)))
                    accel_z.append(float(acc_match.group(3)))

                # Match gyroscope values
                gyro_match = re.search(r"Gyro:\s*(-?\d+\.\d+),\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)", line)
                if gyro_match:
                    gyro_x.append(float(gyro_match.group(1)))
                    gyro_y.append(float(gyro_match.group(2)))
                    gyro_z.append(float(gyro_match.group(3)))

                # Match time values
                time_match = re.search(r"t:\s*(\d+)", line)
                if time_match:
                    time.append(int(time_match.group(1)))

        # Adjust time for increments
        for i in range(0, len(time)):
            time[i] = time[i] + 50 * i

        # Create a DataFrame from parsed data
        data = {
            "Time (ms)": time,
            "Accel_X": accel_x,
            "Accel_Y": accel_y,
            "Accel_Z": accel_z,
            "Gyro_X": gyro_x,
            "Gyro_Y": gyro_y,
            "Gyro_Z": gyro_z,
        }
        df = pd.DataFrame(data)

        # Step 2: Drop duplicates
        df = df.drop_duplicates()
   
        # Step 4: Normalize signals (excluding Time column)
        df = df.iloc[:, 1:]  # Exclude Time column for normalization
     

        # Step 5: Extract features
        cfg = tsfel.get_features_by_domain()
        unwanted_domains = ['spectral']  # Specify the domains you want to exclude
        for domain in unwanted_domains:
            if domain in cfg:
                del cfg[domain]
        features = tsfel.time_series_features_extractor(cfg, df, fs=fs)
  

        # Add a column to identify the file
        features["File"] = os.path.basename(file)
    

        # Append the extracted features to the list
        all_features.append(features)
        
    combined_features = pd.concat(all_features, axis=0)

    combined_features['Class'] = combined_features['File'].apply(assign_class)
        
    # Step 6: Save to a single CSV file
    combined_features.to_csv("combined_features.csv", index=False, sep=";")
   
    return combined_features
    """    
    # Display a preview of the combined features
    print(combined_features.head())
    """
    
def assign_class(file_name):
    # Extrair a classe com base no início do nome do ficheiro
    return file_name.split('_')[0]  # Considera o texto antes do primeiro '_'






extract(directory)
