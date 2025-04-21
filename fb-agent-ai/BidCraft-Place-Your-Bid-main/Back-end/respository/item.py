import os
from sqlalchemy.orm import Session
from fastapi import Response, HTTPException,status
import models, schemas
from hashing import Hash
from datetime import date, datetime

def list_category(id,string_list,db: Session):
    for string in string_list:
        category = db.query(models.Category).filter(models.Category.category_name == string).first()
        new_data = models.ItemCategory(item_id=id,category_id = category.category_id)
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
    return new_data

def list_item(request : schemas.Item, db: Session,seller_id):
    new_item = models.Item(seller_id = seller_id,name = request.name,description = request.description,
                           condition = request.condition,
                           starting_price = request.starting_price,current_bid = request.starting_price,
                           auction_end_date = request.auction_end_date)
    
    file_path = os.path.join(request.pic)
    image_bytes = None
    with open(file_path, 'rb') as f:
        image_bytes = f.read()
    
    # # Save the image bytes to the database
    # if image_bytes:
        new_item.pic = image_bytes

    # Add user to the database
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    num_items = db.query(models.Item).count()
    done = list_category(num_items,request.category,db)

    # Return the created user
    return num_items

def get_item(id,db: Session):
    item = db.query(models.Item).filter(models.Item.item_id == id).first()
    item.auction_end_date = str(item.auction_end_date)
    return item


    

