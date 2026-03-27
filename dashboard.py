# importa libraries
import pandas as pd
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from scipy import stats

warnings.filterwarnings('ignore')

# ===============================
# Professional styling
# ===============================
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

file_path = "battledeaths_global_1946_2025.csv"

df = pd.read_csv(file_path)


# Ajustar estos nombres de columna según lo que tenga el CSV real
# Imprimir primero para confirmar: print(df.columns.tolist())

conflictos_por_anio = (
    df.groupby("year")["conflict_id"]
    .count()
    .reset_index()
    .rename(columns={"conflict_id": "total_conflictos"})
)

resumen = df.groupby("region")["bd_high"].sum().sort_values(ascending=False).head(5)
resumen_texto = resumen.to_string()

prompt = f"""Eres un analista de conflictos armados. 
Con base en este resumen de datos globales, da 5 comprensiones claves y propositivas de las guerras y los genocidios en español, 
de forma clara y directa, sin listas con asteriscos:

Top 5 regiones por muertes en conflictos:
{resumen_texto}

Total de conflictos registrados: {len(df)}
Rango de años: {df['year'].min()} - {df['year'].max()}
"""

payload = {
    "labels": conflictos_por_anio["year"].tolist(),
    "values": conflictos_por_anio["total_conflictos"].tolist(),
    "prompt": prompt
}

resp = requests.post("http://192.168.100.188:8080/analizar", json=payload)
print("Status:", resp.status_code)
print("Respuesta:", resp.text)