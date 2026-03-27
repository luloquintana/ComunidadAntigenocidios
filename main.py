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

# ===============================
# Show Kaggle Input Files
# ===============================
print("Files available in /kaggle/input:\n")

for root, dirs, files in os.walk("/kaggle/input"):
    for file in files:
        print(os.path.join(root, file))

# ===============================
# Load Dataset
# ===============================

file_path = "battledeaths_global_1946_2025.csv"

df = pd.read_csv(file_path)

print("\n✅ Dataset loaded successfully!")

# ===============================
# Initial Data Inspection
# ===============================

print("=" * 80)
print("🌍 GLOBAL BATTLE DEATHS DATASET - COMPREHENSIVE EDA")
print("=" * 80)

print(f"\n📊 Dataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

# Time range check
if "year" in df.columns:
    print(f"\n📅 Time Range: {df['year'].min()} - {df['year'].max()}")
else:
    print("\n⚠️ 'year' column not found")

# Missing values
print("\n🔍 Missing Values:")
missing = df.isnull().sum()
missing = missing[missing > 0]

if len(missing) > 0:
    print(missing)
else:
    print("No missing values found.")

# Column names
print("\n📋 Column Names:")
print(df.columns.tolist())

# Data types
print("\n📝 Data Types:")
print(df.dtypes)

# Preview dataset
print("\n👀 First 5 Rows:")
print(df.head())

# construye el prompt

resumen = df.describe().to_string()
prompt = f"Analiza este dataset y da 3 insights clave en español:\n{resumen}"

resp = requests.post("http://192.168.100.188:8080/analizar", json={"prompt": prompt})

print("Status code:", resp.status_code)
print("Respuesta cruda:", resp.text)  # ← esto muestra qué llegó de verdad

if resp.text:
    print(resp.json())
else:
    print("El servidor devolvió una respuesta vacía")