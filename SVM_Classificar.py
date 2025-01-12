# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:47:35 2024

@author: 35193
"""

from sklearn.preprocessing import StandardScaler
from extractfilesfinal import extract
from Short_features import filter_features
from SVM_Leave_one_out import modelo

# Caminho para os novos dados 
samples_path = r"C:\Users\Diogo Chikhi\OneDrive\Ambiente de Trabalho\Faculdade\4ano\AAI\lab6\dados de teste"

dfn = filter_features(samples_path)

# Separar features (X) e rótulos (y)
Xn = dfn.drop(columns=['File','Class'])



# Normalizar os novos dados usando o mesmo scaler
scaler = StandardScaler()
new_samples_scaled = scaler.fit_transform(Xn)

# Fazer previsões para os novos dados
new_predictions = modelo.predict(Xn)

# Exibir os resultados
print("\nPrevisões para novos dados:")
for i, prediction in enumerate(new_predictions):
    print(f"Amostra {i + 1}: Classe prevista = {prediction}")