import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../spotify_songs.csv")
# Visualizar las primeras filas del DataFrame
print(df.head())

# Información general sobre el DataFrame, incluyendo tipos de datos y valores nulos
print(df.info())

# Resumen estadístico para columnas numéricas
print(df.describe())

# Contar valores nulos en cada columna
print(df.isnull().sum())

# Histograma de algunas variables clave
numerical_columns = ['track_popularity', 'danceability', 'energy', 'loudness',
                     'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                     'valence', 'tempo', 'duration_ms']

df[numerical_columns].hist(bins=15, figsize=(15, 10))
plt.suptitle("Distribución de variables numéricas", y=1.02)
plt.tight_layout()
plt.show()

# Matriz de correlación
correlation_matrix = df[numerical_columns].corr()

# Mapa de calor de la matriz de correlación
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Mapa de calor de la correlación entre variables numéricas")
plt.show()

# Average popularity by playlist genre, sorted in descending order
playlist_popularity = df.groupby('playlist_genre')['track_popularity'].mean().sort_values(ascending=False)

# Plotting with improvements
plt.figure(figsize=(10, 6))
sns.barplot(x=playlist_popularity.values, y=playlist_popularity.index, hue=playlist_popularity.index, palette='magma',
            legend=False)


# Adding data labels
for index, value in enumerate(playlist_popularity.values):
    plt.text(value, index, f'{value:.1f}', va='center', ha='left', color='black')

# Enhancing readability
plt.title('Promedio Popularidad por Género', fontsize=16)
plt.xlabel('Promedio popularidad', fontsize=12)
plt.ylabel('Género Musical', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# Adding gridlines for comparison
plt.grid(axis='x', linestyle='--', alpha=0.7)

plt.show()

#Análisis de la distribución de la duración de las canciones.
plt.figure(figsize=(10, 6))
sns.histplot(df['duration_ms'], bins=30, kde=True)
plt.title("Distribución de la duración de las canciones")
plt.xlabel("Duración (ms)")
plt.ylabel("Frecuencia")
plt.show()

plt.figure(figsize=(14, 6))
sns.boxplot(x='playlist_genre', y='energy', data=df)
plt.title("Distribución de la energía por género de playlist")
plt.xlabel("Género de playlist")
plt.ylabel("Energía")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(14, 6))
sns.boxplot(x='playlist_genre', y='acousticness', data=df)
plt.title("Distribución de la acústica por género de playlist")
plt.xlabel("Género de playlist")
plt.ylabel("Acousticness")
plt.xticks(rotation=45)
plt.show()
