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
import math

router = APIRouter(
    prefix='/save',
    tags=['Saved']
)

@router.post('/save')
def save_item(id,db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
    list = db.query(models.SavedItem).filter(models.SavedItem.item_id == id 
                                             and models.SavedItem.user_id==current_user.user_id).first()
    if list:
        return "Already in save list"
    new_list = models.SavedItem(user_id = current_user.user_id,item_id = id)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list

@router.post('/remove')
def remove_item(id: int, db: Session = Depends(database.get_db), current_user=Depends(oauth2.getCurrentUser)):
    saved_item = db.query(models.SavedItem).filter(
        (models.SavedItem.item_id == id) &
        (models.SavedItem.user_id == current_user.user_id)
    ).first()

    if not saved_item:
        return "Already deleted"

    db.delete(saved_item)
    db.commit()
    return "Item removed from your saved list successfully"

def showItem(id,db: Session):
    item = db.query(models.Item).filter(models.Item.item_id==id).first()
    if item.pic:
        item.pic = base64.b64encode(item.pic).decode('utf-8')
    # item.seller = schemas.UserBase(
    #     name=item.seller.name,
    #     email=item.seller.email,
    #     phone=item.seller.phone
    # )
    return item

@router.get('/mysavelist')
def my_list(db: Session = Depends(database.get_db), current_user=Depends(oauth2.getCurrentUser)):
    items = db.query(models.SavedItem).filter(models.SavedItem.user_id==current_user.user_id).all()
    items.reverse()
    response = []
    for item in items:
        showi = showItem(item.item_id,db)
        response.append(showi)
    return response