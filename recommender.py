from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from config import SessionLocal
from models import Song
import pandas as pd

# Recomendación basada en contenido
def get_recommendations(song_id, top_n=5):
    session = SessionLocal()
    songs = session.query(Song).all()
    session.close()

    # Crear un DataFrame con las características
    df = pd.DataFrame([{
        'id': song.id,
        'tempo': song.tempo,
        'loudness': song.loudness,
        'valence': song.valence,
        'speechiness': song.speechiness,
        'acousticness': song.acousticness,
        'instrumentalness': song.instrumentalness,
        'duration_ms': song.duration_ms
    } for song in songs])

    # Verifica si el song_id existe en el DataFrame
    if song_id not in df['id'].values:
        raise ValueError(f"El song_id '{song_id}' no existe en el DataFrame")

    # Seleccionar la fila de la canción para comparación
    song_vector = df[df['id'] == song_id].drop(columns=['id']).values
    song_features = df.drop(columns=['id']).values

    # Similaridad de coseno
    similarities = cosine_similarity(song_vector, song_features).flatten()
    similar_indices = similarities.argsort()[::-1][1:top_n+1]  # Ignorar la primera

    return df.iloc[similar_indices]['id'].tolist()
