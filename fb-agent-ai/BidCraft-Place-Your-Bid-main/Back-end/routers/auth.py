from datetime import date
import models
import schemas
import utils
import oauth2
import database
from hashing import Hash
from fastapi import Depends, HTTPException, APIRouter,status
from sqlalchemy.orm import Session
import random
import string

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/signin", response_model=schemas.Token)
def signin(credential: schemas.SingIn,db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        (models.User.email == credential.user_id) |
        (models.User.user_id == credential.user_id)
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User not found with {credential.user_id}")
    if not Hash.verify(credential.password, user.password):
        raise HTTPException(status_code=404, detail="Incorect passeword")

    access_token = oauth2.createAccessToken(
        data={"user_id": user.user_id,"email": user.email, "name": user.name, "phone": user.phone})

    tokenData = schemas.Token(name=user.name, email=user.email,
                              accessToken=access_token, phone=user.phone, token_type="Bearer", user_id=user.user_id)
    return tokenData

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user(current_user: str = Depends(oauth2.getCurrentUser)):

    oauth2.blacklist_token(current_user)
    return {"message": "User logged out successfully"}

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def Signup(request: schemas.SignUp,db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        (models.User.user_id == request.phone) |
        (models.User.email == request.email)
    ).first()

    if user:
       if user.phone == request.phone:
           raise HTTPException(status_code=status.HTTP_302_FOUND,detail=f'You already registerd with {user.phone}. Goto login page')
       if user.email == request.email:
           raise HTTPException(status_code=status.HTTP_302_FOUND,detail=f'You already registerd with {user.email}. Goto login page')
    else:
        random_password = generate_password()
        hassPassword = Hash.bcrypt(random_password)
        new_user = models.User(user_id = request.phone,name = request.name,email = request.email,
                           phone = request.phone,password = hassPassword,dob = request.dob)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        utils.sendEmail("Welcome to our platform",
                    f"Hello {request.name}, Welcome to our platform. Your one password is \n{random_password}\nYou can use this password to login to our platform. Thank you.", request.email)
        
        return 'Check your email [also in Spam Box] for password'

@router.put("/change_password", status_code=status.HTTP_202_ACCEPTED)
def change_password(request: schemas.ConfirmPass, db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
    id = current_user.user_id
    user = db.query(models.User).filter(models.User.user_id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if request.password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    hashed_password = Hash.bcrypt(request.password)
    user.password = hashed_password
    db.commit()
    return {"message": "Password updated successfully"}

@router.post('/forget_password',status_code=status.HTTP_226_IM_USED)
def recover_id(request : schemas.Userid,db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User not with {request.user_id}')
    else:
        random_password = generate_password()
        hassPassword = Hash.bcrypt(random_password)
        user.password = hassPassword
        db.commit()
        utils.sendEmail("Recovery Password",
                    f"Hello {user.name},Your recover password is \n{random_password}\nYou can use this password to login to our platform. Thank you.", user.email)
        
        return 'Check your email [also in Spam Box] for password'
    
