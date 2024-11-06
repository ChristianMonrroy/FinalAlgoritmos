from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(String, unique=True, index=True)
    track_name = Column(String)
    track_artist = Column(String)
    track_popularity = Column(Integer)
    playlist_genre = Column(String)
    tempo = Column(Float)
    duration_ms = Column(Integer)
    loudness = Column(Float)
    speechiness = Column(Float)
    acousticness = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    valence = Column(Float)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    preferences = relationship("Preference", back_populates="user")

class Preference(Base):
    __tablename__ = "preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    song_id = Column(Integer, ForeignKey("songs.id"))
    rating = Column(Float)  # Rating del usuario para una canción
    user = relationship("User", back_populates="preferences")
    song = relationship("Song")
