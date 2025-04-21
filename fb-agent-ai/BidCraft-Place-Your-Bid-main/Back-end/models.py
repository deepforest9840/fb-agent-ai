from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Date, LargeBinary, Boolean, Index,Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    user_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String,unique=True)
    phone = Column(String, unique=True)
    pic = Column(LargeBinary)
    password = Column(String)
    dob = Column(String)

    addresses = relationship("Address", back_populates="user")
    items = relationship("Item", back_populates="seller")
    bids = relationship("Bid", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    saved_items = relationship("SavedItem", back_populates="user")
    questions = relationship("Question", back_populates="user")
    answers = relationship("Answer", back_populates="user")
    comments = relationship("Comment", back_populates="user")


class Address(Base):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('user.user_id'))
    address = Column(String)

    user = relationship("User", back_populates="addresses")

class Item(Base):
    __tablename__ = 'item'

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(String, ForeignKey('user.user_id'))
    name = Column(String)
    description = Column(String)
    condition = Column(String)
    pic = Column(LargeBinary)
    starting_price = Column(Float)
    current_bid = Column(Float)
    auction_end_date = Column(String)
    winner_id = Column(String)

    seller = relationship("User", back_populates="items")
    bids = relationship("Bid", back_populates="item")
    categories = relationship("Category", secondary="item_category", back_populates="items")
    payments = relationship("Payment", back_populates="item")
    questions = relationship("Question", back_populates="item")
    comments = relationship("Comment", back_populates="item")

class Bid(Base):
    __tablename__ = 'bid'

    bid_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('item.item_id'))
    user_id = Column(String, ForeignKey('user.user_id'))
    bid_amount = Column(Float)
    bid_time = Column(String)

    item = relationship("Item", back_populates="bids")
    user = relationship("User", back_populates="bids")

class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String)

    items = relationship("Item", secondary="item_category", back_populates="categories")

class ItemCategory(Base):
    __tablename__ = 'item_category'

    item_id = Column(Integer, ForeignKey('item.item_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('category.category_id'), primary_key=True)

class Payment(Base):
    __tablename__ = 'payment'

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('user.user_id'))
    item_id = Column(Integer, ForeignKey('item.item_id'))
    payment_amount = Column(Float)
    payment_time = Column(String)
    payment_method = Column(String)
    payment_status = Column(String)

    user = relationship("User", back_populates="payments")
    item = relationship("Item", back_populates="payments")

class Notification(Base):
    __tablename__ = 'notification'

    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('user.user_id'))
    notification_message = Column(String)
    notification_time = Column(String)
    read_status = Column(Boolean)

    user = relationship("User", back_populates="notifications")

class SavedItem(Base):
    __tablename__ = 'saved_item'

    user_id = Column(String, ForeignKey('user.user_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.item_id'), primary_key=True)

    user = relationship("User", back_populates="saved_items")


class Question(Base):
    __tablename__ = 'question'

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('item.item_id'))
    user_id = Column(String, ForeignKey('user.user_id'))
    question_text = Column(String)
    timestamp = Column(String)

    # Define many-to-one relationship with item
    item = relationship("Item", back_populates="questions")

    # Define many-to-one relationship with user
    user = relationship("User", back_populates="questions")

    # Define one-to-one relationship with answer
    answer = relationship("Answer", uselist=False, back_populates="question")


class Answer(Base):
    __tablename__ = 'answer'

    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('question.question_id'))
    user_id = Column(String, ForeignKey('user.user_id'))
    answer_text = Column(String)
    timestamp = Column(String)

    # Define many-to-one relationship with user
    user = relationship("User", back_populates="answers")

    # Define many-to-one relationship with question
    question = relationship("Question", back_populates="answer")

class Comment(Base):
    __tablename__ = 'comment'

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('item.item_id'))
    user_id = Column(String, ForeignKey('user.user_id'))
    text = Column(Text)
    timestamp = Column(String)

    # Define many-to-one relationship with user
    user = relationship("User", back_populates="comments")
    # Define many-to-one relationship with item
    item = relationship("Item", back_populates="comments")

class Rating(Base):
    __tablename__ = 'rating'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id_from = Column(String, ForeignKey('user.user_id'))
    user_id_to = Column(String, ForeignKey('user.user_id'))
    rating = Column(Integer)
    text = Column(Text)
    timestamp = Column(String)

    user_from = relationship('User', foreign_keys=[user_id_from])
    user_to = relationship('User', foreign_keys=[user_id_to])