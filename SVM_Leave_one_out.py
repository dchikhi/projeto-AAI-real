# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:34:32 2024

@author: 35193
"""

import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
#from Short_features import filter_features

# Caminho do arquivo
file_path = 'filtered_features_treino.csv'

# Carregar o arquivo filtrado
df = pd.read_csv(file_path, sep=';')

# Separar features (X) e rótulos (y)
X = df.drop(columns=['File', 'Class'])
y = df['Class']

# Criar o modelo SVM
svm_model = SVC(kernel='linear')

# Leave-One-Out cross-validation
loo = LeaveOneOut()
y_true = []
y_pred = []

# Iterar sobre cada divisão do Leave-One-Out
for train_index, test_index in loo.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    # Treinar o modelo
    svm_model.fit(X_train, y_train)
    
    # Fazer previsões
    y_pred.append(svm_model.predict(X_test)[0])
    y_true.append(y_test.iloc[0])
    
modelo = svm_model.fit(X_train, y_train)   
    
# Avaliar o modelo
accuracy = accuracy_score(y_true, y_pred)
print(f"Precisão do modelo: {accuracy * 100:.2f}%")
print("\nRelatório de classificação:")
print(classification_report(y_true, y_pred))

# Matriz de confusão
conf_matrix = confusion_matrix(y_true, y_pred)
print("\nMatriz de Confusão:")
print(conf_matrix)

# Visualizar a matriz de confusão
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=svm_model.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.title("Matriz de Confusão")
plt.show()
