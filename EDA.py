import pandas as pd
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

resp = requests.get("https://data.techforpalestine.org/api/v3/killed-in-gaza.min.json") # jala datos en formato j   son

data = json.loads(resp.text) # convierte a formato json    
print(data) 


