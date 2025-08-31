from fastapi import FastAPI,HTTPException, Depends
from typing import List, Annotated
import models
import db
from db import engine, SessionLocal
from sqlalchemy.orm import Session
import schemas

app = FastAPI()
db.create_tables()

@app.get("/questions/{questions_id}")
async def read_questions(question_id: int, db: Annotated[Session,Depends(db.get_db)]):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code = 404, detail = "Question is not found" )
    return result

@app.get("/choices/{questions_id}")
async def read_choices(question_id: int, db: Annotated[Session,Depends(db.get_db)]):
    result = db.query(models.Choices).filter(models.Questions.id == question_id).all()
    if not result:
        raise HTTPException(status_code = 404, detail = "Choices is not found" )
    return result

@app.post("/questions/")
async def create_questions(question:schemas.QuestionBase,db: Annotated[Session, Depends(db.get_db)]):
    db_question = models.Questions(question_text = question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(choice_text = choice.choice_text, is_correct = choice.is_correct, question_id = db_question.id)
        db.add(db_choice)
    db.commit()

 