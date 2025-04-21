from datetime import datetime
from fastapi import APIRouter, Depends,status,HTTPException,Response
from typing import List
from passlib.context import CryptContext
from respository import item
from sqlalchemy.orm import Session
import schemas,database,models,oauth2

router = APIRouter(
    prefix='/item',
    tags=['Q&A']
)

def getans(id,db: Session):
    ans = db.query(models.Answer).filter(models.Answer.question_id==id).all()
    return ans

@router.post('/question',status_code=status.HTTP_201_CREATED)
def post_question(id,request : schemas.Question,db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
    now = datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    new_quetion = models.Question(item_id = id,user_id=current_user.user_id,question_text = request.question_text,timestamp=current_datetime)
    db.add(new_quetion)
    db.commit()
    db.refresh(new_quetion)
    return new_quetion

@router.post('/answer',status_code=status.HTTP_201_CREATED)
def post_answer(id,request : schemas.Answer,db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
    now = datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    new_answer = models.Answer(question_id = id,user_id=current_user.user_id, answer_text = request.answer_text,timestamp=current_datetime)
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer

@router.get('/QA', response_model=List[schemas.showQA], status_code=status.HTTP_302_FOUND)
def get_qa(item_id: int, db: Session = Depends(database.get_db)):
    ques = db.query(models.Question).filter(models.Question.item_id==item_id).all()
    for que in ques:
        ans = getans(que.question_id,db)
        que.answers = ans

    return ques