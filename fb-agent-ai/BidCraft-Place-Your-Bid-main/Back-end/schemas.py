from pydantic import BaseModel, EmailStr
from typing import List, Optional


class Userid(BaseModel):
    user_id : str


class UserBase(BaseModel):
    name : str
    email : EmailStr
    phone : str
    class Config:
        orm_mode = True

class SignUp(UserBase):
    dob : str
    class Config:
        orm_mode : True

class ConfirmPass(BaseModel):
    password : str
    confirm_password : str

class Addimage(BaseModel):
    pic : str

class User(SignUp):
    password : str

class Category(BaseModel):
    name : str


class ItemBase(BaseModel):
    name : str
    description : str
    condition : str
    starting_price : float
    auction_end_date : str

    class Config:
        orm_mode = True

class itemShow(ItemBase):
    item_id : int
    current_bid : float
    class Config:
        orm_mode = True
        
class ShowCategory(Category):
    items : List[itemShow] = []
    class Config:
        orm_mode : True

class Item(ItemBase):
    pic : str
    category : List[str] = []
    class Config:
        orm_mode : True

class showInmain(ItemBase):
    pic : Optional[bytes]
    item_id : int
    current_bid : float
    seller : UserBase

    class Config:
        orm_mode : True

class Address(BaseModel):
    house_no : str
    road : str
    upazilla : str
    district : str

# class ShowMyItem(UserBase):
#     items = List[ItemBase] = []
#     class Config:
#         orm_mode = True

class SingIn(BaseModel):
    user_id : str
    password : str

    class Config:
        orm_mode = True

class Token(BaseModel):
    accessToken: str
    token_type: str
    email: EmailStr
    user_id : str
    name: str
    phone: str

class TokenData(BaseModel):
    user_id : str


class payload(BaseModel):
    user_id : str
    email: EmailStr
    phone: str
    name: str

    class Config:
        orm_mode = True

class Question(BaseModel):
    question_text : str

    class Config:
        orm_mode : True

class Answer(BaseModel):
    answer_text : str
    
    class Config:
        orm_mode : True

class NameUser(BaseModel):
    name : str
    class Config:
        orm_mode : True

class getQuetion(BaseModel):
    question_id : int
    item_id : int
    question_text : str
    timestamp : str
    user : UserBase

class getAnswer(BaseModel):
    answer_id : int
    question_id : int
    answer_text : str
    timestamp : str
    user : UserBase
    class Config:
        orm_mode : True

class showQA(getQuetion):
    answers : List[getAnswer] = []
    class Config:
        orm_mode : True

class Comment(BaseModel):
    text : str
    class Config:
        orm_mode : True

class showComment(Comment):
    item_id : int
    user : UserBase
    timestamp : str
    class Config:
        orm_mode : True

class showItem(ItemBase):
    item_id : int
    pic : Optional[bytes]
    current_bid : float
    seller : UserBase
    qa : List[showQA] = []
    comments : List[showComment] = []

    class Config:
        orm_mode : True

class Rate(BaseModel):
    rating : int
    text : str
    class Config:
        orm_mode : True

class Rating(Rate):
    user_id_from : str

class showRating(Rate):
    user_from : UserBase
    class Config:
        orm_mode : True
    
class search(BaseModel):
    text : str
    class Config:
        orm_mode : True

class filter(BaseModel):
    price : int
    class Config:
        orm_mode : True

class UserDetails(UserBase):
    pic : Optional[bytes]
    overall_rating : float
    rates : List[showRating] = []
    items : List[showInmain] = []
    class Config:
        orm_mode : True

class MyDetails(UserDetails):
    dob : str
    class Config:
        orm_mode : True

class Bid(BaseModel):
    item_id : int
    bid_amount : float
    class Config:
        orm_mode : True

class getBid(Bid):
    bid_id : int
    bid_time : str
    user : UserBase
    class Config:
        orm_mode : True

class getMyBid(Bid):
    bid_id : int
    bid_time : str
    item : ItemBase

    class Config:
        orm_mode : True

class getSaveItem(BaseModel):
    items : List[showInmain] = []
    class Config:
        orm_mode = True