from datetime import datetime
from fastapi import APIRouter, Depends,status,HTTPException,Response
from typing import List
from passlib.context import CryptContext
from respository import user
from sqlalchemy.orm import Session
import schemas,database,models
import oauth2
from hashing import Hash

router = APIRouter(
    prefix='/rate',
    tags=['rating']
)

@router.post('/give',status_code=status.HTTP_201_CREATED)
def post_comment(request : schemas.Rating,db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
    rate = db.query(models.Rating).filter(models.Rating.user_id_from==current_user.user_id and 
                                          models.Rating.user_id_to==request.user_id_to).first()
    if not rate:
        now = datetime.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        new_rate = models.Rating(user_id_to = request.user_id_from,user_id_from=current_user.user_id,rating = request.rating,text = request.text,timestamp=current_datetime)
        db.add(new_rate)
        db.commit()
        db.refresh(new_rate)
        return new_rate
    else:
        rate.text = request.text
        rate.rating = request.rating
        db.commit()
        return rate
