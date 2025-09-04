from pydantic import BaseModel
from typing import List

class ActorBase(BaseModel):
    name: str
    birth_year: int

class ActorCreate(ActorBase):
    pass

class Actor(ActorBase):
    id: int

    class Config:
        from_attributes = True


class MovieBase(BaseModel):
    title: str
    release_year: int
    genre: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    actors: List[Actor] = []

    class Config:
        from_attributes = True
