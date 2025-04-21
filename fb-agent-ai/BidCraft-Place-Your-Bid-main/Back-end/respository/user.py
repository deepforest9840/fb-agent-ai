from sqlalchemy.orm import Session
from fastapi import Response, HTTPException,status
import models, schemas
from hashing import Hash
from datetime import date, datetime

def create_user(request : schemas.User, db: Session):
    # Create a new user object
    hassPassword = Hash.bcrypt(request.password)
    request.password = hassPassword
    new_user = models.User(user_id = request.phone,name = request.name,email = request.email,
                           phone = request.phone,password = hassPassword,dob = request.dob)

    # Add user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the created user
    return new_user

def list_add(request : schemas.Address, db: Session,id):
    address = ''
    address = address+'House_no: '+request.house_no+'\nRoad: '+request.road+'\nUpazilla: '+request.upazilla+'\nDistrict: '+request.district
    list_add = models.Address(user_id = id,address = address)
    db.add(list_add)
    db.commit()
    db.refresh(list_add)

    return list_add


