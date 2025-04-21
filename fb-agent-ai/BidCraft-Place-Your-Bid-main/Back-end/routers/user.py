import base64
import os
from fastapi import APIRouter, Depends,status,HTTPException,Response
from typing import List
from passlib.context import CryptContext
from sqlalchemy import desc
from respository import user
from sqlalchemy.orm import Session
import schemas,database,models
import oauth2
from hashing import Hash

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/create',status_code=status.HTTP_201_CREATED)
def create_user(request : schemas.User,db: Session = Depends(database.get_db)):
    new_user =  user.create_user(request,db)
    if not new_user:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f'User not created')
    else:
        return 'created'

@router.post('/list_add',status_code=status.HTTP_201_CREATED)
def create_user(request : schemas.Address,db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
    new_add =  user.list_add(request,db,current_user.user_id)
    if not new_add:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f'User not created')
    else:
        return 'listed'
    
@router.get('/items',response_model=List[schemas.itemShow],status_code=status.HTTP_302_FOUND)
def my_item(db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
   items = db.query(models.Item)\
              .filter(models.Item.seller_id == current_user.user_id)\
              .order_by(desc(models.Item.auction_end_date))\
              .all()
   if items:
       for item in items:
           if item.pic:
               item.pic = base64.b64encode(item.pic).decode('utf-8')
       return items
   else:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='You have listed no item yet')


@router.post('/change_image', status_code=status.HTTP_201_CREATED)
def change_image(request: schemas.Addimage, db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
    user = db.query(models.User).filter(models.User.user_id == current_user.user_id).first()
    
    # Construct the file path using os.path.join
    file_path = os.path.join(request.pic)
    
    # Open the image file
    image_bytes = None
    with open(file_path, 'rb') as f:
        image_bytes = f.read()
    
    # # Save the image bytes to the database
    # if image_bytes:
        user.pic = image_bytes
        db.commit()
        db.refresh(user)
    
    return {"message": "Image uploaded successfully"}

@router.get('/show_my_profile', response_model=schemas.MyDetails)
def show_my_profile(db: Session = Depends(database.get_db), current_user=Depends(oauth2.getCurrentUser)):
    user = db.query(models.User).filter(models.User.user_id == current_user.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    rates = db.query(models.Rating).filter(models.Rating.user_id_to == current_user.user_id).all()
    user.rates = rates
    items = db.query(models.Item)\
              .filter(models.Item.seller_id == user.user_id)\
              .order_by(desc(models.Item.auction_end_date))\
              .all()
    for item in items:
        if item.pic:
            item.pic = base64.b64encode(item.pic).decode('utf-8')
    user.items = items
    # Encode pic if it exists
    if user.pic:
        user.pic = base64.b64encode(user.pic).decode('utf-8')

    # Calculate overall rating
    num = len(rates)
    rating_sum = sum(rate.rating for rate in rates) if num > 0 else 0
    user.overall_rating = rating_sum / num if num > 0 else 0.0

    return user

@router.post('/show_profile', response_model=schemas.UserDetails)
def show_profile(request : schemas.NameUser,db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.user_id == request.name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    rates = db.query(models.Rating).filter(models.Rating.user_id_to == user.user_id).all()
    items = db.query(models.Item)\
              .filter(models.Item.seller_id == user.user_id)\
              .order_by(desc(models.Item.auction_end_date))\
              .all()
    for item in items:
        if item.pic:
            item.pic = base64.b64encode(item.pic).decode('utf-8')
    user.items = items
    user.rates = rates

    if user.pic:
        user.pic = base64.b64encode(user.pic).decode('utf-8')

    num = len(rates)
    rating_sum = sum(rate.rating for rate in rates) if num > 0 else 0
    user.overall_rating = rating_sum / num if num > 0 else 0.0

    return user