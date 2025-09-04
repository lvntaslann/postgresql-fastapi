from sqlalchemy import Column, Integer, String, Table, ForeignKey
from db import Base
from sqlalchemy.orm import relationship

movie_actors = Table(
    'movie_actors',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    release_year = Column(Integer)
    genre = Column(String)

    actors = relationship('Actor', secondary=movie_actors, back_populates='movies')

class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    birth_year = Column(Integer)

    movies = relationship('Movie', secondary=movie_actors, back_populates="actors")
