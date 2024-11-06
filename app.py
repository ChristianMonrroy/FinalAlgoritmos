import pandas as pd
from flask import Flask, jsonify, request
from sqlalchemy.orm import Session
from config import SessionLocal
from models import Song
from recommender import get_recommendations

app = Flask(__name__)

# Cargar las canciones desde el archivo CSV a la base de datos
def load_songs():
    session = SessionLocal()
    try:
        # Cargar el CSV
        df = pd.read_csv("spotify_songs.csv")
        print("Primeras filas del dataset:", df.head())

        # Eliminar duplicados en track_id
        if df.duplicated(subset=['track_id']).any():
            print("Hay duplicados en track_id. Eliminándolos...")
            df = df.drop_duplicates(subset=['track_id'])

        # Insertar cada canción en la base de datos
        for _, row in df.iterrows():
            song = Song(
                track_id=row['track_id'],
                track_name=row['track_name'],
                track_artist=row['track_artist'],
                track_popularity=row['track_popularity'],
                playlist_genre=row['playlist_genre'],
                tempo=row['tempo'],
                duration_ms=row['duration_ms'],
                loudness=row['loudness'],
                speechiness=row['speechiness'],
                acousticness=row['acousticness'],
                instrumentalness=row['instrumentalness'],
                liveness=row['liveness'],
                valence=row['valence']
            )
            session.add(song)

        session.commit()
        print("Canciones cargadas exitosamente en la base de datos.")

    except Exception as e:
        print("Error al cargar canciones en la base de datos:", e)

    finally:
        session.close()

# Llamar esta función solo una vez para cargar las canciones
#load_songs()

# Ruta de recomendación
@app.route('/recommend', methods=['GET'])
def recommend():
    song_id = request.args.get('song_id', type=int)
    recommendations = get_recommendations(song_id)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
