from pydantic import BaseModel

class BookBase(BaseModel):
    title:str
    author:str
    description:str
    year:int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id:int

    class config:
        # orm_mode = True # pydantic version < 2.x
        from_attribute = True # pydantic version > 2.x