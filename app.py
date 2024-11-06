import pandas as pd
from flask import Flask, jsonify, request
from sqlalchemy.orm import Session
from config import SessionLocal
from models import Song
from recommender import get_recommendations

app = Flask(__name__)

# Cargar las canciones desde el dataset CSV a la base de datos
def load_songs():
    session = SessionLocal()
    df = pd.read_csv("CSV/spotify_songs.csv")  # Cambia este nombre si el archivo tiene otro nombre
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
    session.close()

# Llamar esta función solo una vez para cargar las canciones
# load_songs()

# Ruta de recomendación de canciones
@app.route('/recommend', methods=['GET'])
def recommend():
    song_id = request.args.get('song_id', type=int)
    recommendations = get_recommendations(song_id)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
