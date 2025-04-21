import base64
from datetime import datetime
import os
from fastapi import APIRouter, Depends,status,HTTPException,Response
from typing import List
from passlib.context import CryptContext
from sqlalchemy import desc
from respository import item
from sqlalchemy.orm import Session
import schemas,database,models,oauth2

router = APIRouter(
    prefix='/item',
    tags=['item']
)

def getans(id,db: Session):
    ans = db.query(models.Answer).filter(models.Answer.question_id==id).all()
    return ans

def get_qaa(item_id: int, db: Session):
    ques = db.query(models.Question).filter(models.Question.item_id==item_id).all()
    for que in ques:
        ans = getans(que.question_id,db)
        que.answers = ans
    return ques

def get_comment(id,db: Session):
    comments = db.query(models.Comment).filter(models.Comment.item_id==id).all()
    return comments

@router.post('/create',status_code=status.HTTP_201_CREATED)
def create_item(request : schemas.Item,db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
    new_item =  item.list_item(request,db,current_user.user_id)
    if not new_item:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f'User not created')
    else:
        return f'Item listed with user id {new_item}'

@router.get('/get_item',response_model=schemas.showItem,status_code=status.HTTP_302_FOUND)
def get_item_details(id,db: Session = Depends(database.get_db)):
    item_details =  db.query(models.Item).filter(models.Item.item_id==id).first()
    if not item_details:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f'User not created')
    else:
        qanda = get_qaa(item_details.item_id,db)
        comments = get_comment(item_details.item_id,db)
        item_details.qa = qanda
        item_details.comments = comments
        if item_details.pic:
            item_details.pic = base64.b64encode(item_details.pic).decode('utf-8')
        return item_details
    

@router.post('/comment',status_code=status.HTTP_201_CREATED)
def post_comment(id,request : schemas.Comment,db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
    now = datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    new_comment = models.Comment(item_id = id,user_id=current_user.user_id, text = request.text,timestamp=current_datetime)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get('/comment_show',response_model=List[schemas.showComment],status_code=status.HTTP_201_CREATED)
def show_comment(id,db: Session = Depends(database.get_db)):
    comments = db.query(models.Comment).filter(models.Comment.item_id==id).all()
    return comments

@router.get('/get_items', response_model=List[schemas.showInmain], status_code=status.HTTP_200_OK)
def get_items(db: Session = Depends(database.get_db)):
    items = db.query(models.Item).order_by(models.Item.auction_end_date.desc()).all()
    for item in items:
        if item.pic:
            item.pic = base64.b64encode(item.pic).decode('utf-8')
    return items

@router.post('/search_items', response_model=List[schemas.showInmain], status_code=status.HTTP_200_OK)
def search_items(request: schemas.search, db: Session = Depends(database.get_db)):
    search_text = request.text
    items = db.query(models.Item)\
              .filter(models.Item.name.ilike(f'%{search_text}%'))\
              .order_by(desc(models.Item.auction_end_date))\
              .all()
    for item in items:
        if item.pic:
            item.pic = base64.b64encode(item.pic).decode('utf-8')
    return items

@router.post('/filter_items', response_model=List[schemas.showInmain], status_code=status.HTTP_200_OK)
def filter_items(request: schemas.filter, db: Session = Depends(database.get_db)):
    max_price = request.price
    items = db.query(models.Item)\
              .filter(models.Item.starting_price < max_price)\
              .order_by(desc(models.Item.auction_end_date))\
              .all()
    for item in items:
        if item.pic:
            item.pic = base64.b64encode(item.pic).decode('utf-8')
    return items

@router.post('/change_image', status_code=status.HTTP_201_CREATED)
def change_image(id,request: schemas.Addimage, db: Session = Depends(database.get_db)):
    item = db.query(models.Item).filter(models.Item.item_id == id).first()
    
    # Construct the file path using os.path.join
    file_path = os.path.join(request.pic)
    
    # Open the image file
    image_bytes = None
    with open(file_path, 'rb') as f:
        image_bytes = f.read()
    
    # # Save the image bytes to the database
    # if image_bytes:
        item.pic = image_bytes
        db.commit()
        db.refresh(item)
    
    return {"message": "Image uploaded successfully"}