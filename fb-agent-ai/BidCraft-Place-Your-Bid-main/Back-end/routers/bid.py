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
    prefix='/bid',
    tags=['Bid']
)

@router.post('/new', status_code=status.HTTP_201_CREATED)
def create_bid(request: schemas.Bid, db: Session = Depends(database.get_db), current_user = Depends(oauth2.getCurrentUser)):
    item = db.query(models.Item).filter(models.Item.item_id == request.item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    elif item.seller_id == current_user.user_id:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not allowed")
    elif request.current_bid <= (item.current_bid+1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Enter a bid amount higher than {item.current_bid+1}")
    else:
        now = datetime.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        new_bid = models.Bid(item_id=request.item_id, user_id=current_user.user_id, bid_amount=request.current_bid, bid_time=current_datetime)
        item.current_bid = request.bid_amount
        item.winner_id = current_user.user_id
        db.add(new_bid)
        db.commit()
        db.refresh(new_bid)
        return new_bid
    
@router.get('/get_bid', response_model=List[schemas.getBid])
def get_bid(id: int, db: Session = Depends(database.get_db)):
    bids = db.query(models.Bid).filter(models.Bid.item_id == id).order_by(desc(models.Bid.bid_amount)).all()
    return bids

@router.get('/get_my_bid',response_model=List[schemas.getMyBid])
def get_my_bid(db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
    bids = db.query(models.Bid).filter(models.Bid.user_id == current_user.user_id).order_by(desc(models.Bid.bid_id)).all()
    return bids

@router.get('/get_my_bid_item',response_model=List[schemas.getMyBid])
def get_my_bid_item(id,db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
    bids = db.query(models.Bid).filter(models.Bid.user_id == current_user.user_id and 
                                       models.Bid.item_id == id).order_by(desc(models.Bid.bid_id)).all()
    return bids