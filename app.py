import pandas as pd
from flask import Flask, jsonify, request, render_template
from sqlalchemy.orm import Session
from config import SessionLocal
from models import Song
from recommender import get_recommendations

app = Flask(__name__)

# Ruta para la página principal que renderiza el HTML
@app.route('/')
def home():
    return render_template("index.html")

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

@app.route('/recommend_by_name', methods=['GET'])
def recommend_by_name():
    artist = request.args.get('artist')
    song_name = request.args.get('song')

    session = SessionLocal()
    # Buscar el song_id basado en el artista y nombre de la canción
    song = session.query(Song).filter(Song.track_artist == artist, Song.track_name == song_name).first()

    if not song:
        session.close()
        return jsonify({"error": "Canción no encontrada"}), 404

    # Obtener recomendaciones (IDs) y luego los detalles de cada recomendación
    recommendations_ids = get_recommendations(song.id)
    recommendations = session.query(Song.track_name, Song.track_artist, Song.track_id).filter(Song.id.in_(recommendations_ids)).all()
    session.close()

    # Formatear las recomendaciones incluyendo el enlace de Spotify
    recommendations_list = [
        {
            "track_name": rec.track_name,
            "track_artist": rec.track_artist,
            "spotify_link": f"https://open.spotify.com/track/{rec.track_id}"
        }
        for rec in recommendations
    ]

    # También incluir el enlace de la canción seleccionada
    selected_song = {
        "track_name": song.track_name,
        "track_artist": song.track_artist,
        "spotify_link": f"https://open.spotify.com/track/{song.track_id}"
    }

    return jsonify({"selected_song": selected_song, "recommendations": recommendations_list})


@app.route('/artists', methods=['GET'])
def get_artists():
    session = SessionLocal()
    # Obtener artistas únicos
    artists = session.query(Song.track_artist).distinct().all()
    session.close()
    return jsonify([artist[0] for artist in artists])  # Devolver solo nombres de artistas

@app.route('/songs', methods=['GET'])
def get_songs_by_artist():
    artist = request.args.get('artist')
    session = SessionLocal()
    # Obtener canciones del artista seleccionado
    songs = session.query(Song.track_name).filter(Song.track_artist == artist).all()
    session.close()
    return jsonify([song[0] for song in songs])  # Devolver solo nombres de canciones


if __name__ == "__main__":
    app.run(debug=True)

