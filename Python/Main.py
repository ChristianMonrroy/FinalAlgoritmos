import numpy as np
import pandas as pd
import os
import kaggle
import zipfile

ruta_zip = "../30000-spotify-songs.zip"
ruta_extraccion = "../CSV"
os.makedirs(ruta_extraccion, exist_ok=True)
with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
    for file in zip_ref.namelist():
        if file.endswith(".csv"):
            zip_ref.extract(file, ruta_extraccion)

df = pd.read_csv("../CSV/spotify_songs.csv")
print(df.head())