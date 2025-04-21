from sqlalchemy.orm import Session
from fastapi import Response, HTTPException,status
import models, schemas
from hashing import Hash
from datetime import date, datetime

def list_category(request : schemas.Item, db: Session):
    new_category = models.Category(category_name = request.name)

    # Add user to the database
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    # Return the created user
    return new_category

