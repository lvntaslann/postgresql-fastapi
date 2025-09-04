from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db, create_tables
from models import Movie as MovieModel, Actor as ActorModel
from schemas import MovieCreate, Movie, ActorCreate, Actor

create_tables()
app = FastAPI(title="Film ve Oyuncu Yönetim Sistemi")

"""
MOVIES
"""
@app.post("/movies/", response_model=Movie)
async def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = MovieModel(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/", response_model=list[Movie])
async def get_movies(db: Session = Depends(get_db)):
    return db.query(MovieModel).all()

@app.get("/movies/{movie_id}", response_model=Movie)
async def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

"""
ACTORS
"""
@app.post("/actors/", response_model=Actor)
async def create_actor(actor: ActorCreate, db: Session = Depends(get_db)):
    db_actor = ActorModel(**actor.dict())
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor

@app.get("/actors/", response_model=list[Actor])
async def get_actors(db: Session = Depends(get_db)):
    return db.query(ActorModel).all()

"""
ADD ACTOR TO MOVIE
"""
@app.post("/movies/{movie_id}/actors/{actor_id}", response_model=Movie)
async def add_actor_to_movie(movie_id: int, actor_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    actor = db.query(ActorModel).filter(ActorModel.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")

    movie.actors.append(actor)
    db.commit()
    db.refresh(movie)
    return movie
