from server.db.db import Base, engine, db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


# class Users(Base):
#     __tablename__ = "Users"
#     user_id = Column(Integer, primary_key=True)
#     name = Column(String, index=True)
#     chess_username = Column(String, index=True)
#     email = Column(String, index=True)
#     password = Column(String, nullable=False)
#     start_timestamp = Column(DateTime, default=datetime.utcnow)
    
#     # Defining relationship
#     ratings = relationship("Rating", back_populates="user")
#     # images = relationship("Image", back_populates="user")

class Users(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    chess_username = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, nullable=False)
    avatar = Column(String, nullable= True)
    player_id = Column(String, nullable =True)
    url = Column(String, nullable =True)
    followers = Column(Integer, nullable =True)
    country = Column(String, nullable =True)
    last_online = Column(DateTime, nullable =True)
    joined = Column(DateTime, nullable =True)
    start_timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable =True)
    is_streamer = Column(Boolean, nullable =True)
    verified = Column(Boolean, nullable =True)
    league = Column(String, nullable =True)
    # Defining relationship
    ratings = relationship("Rating", back_populates="user")
    # images = relationship("Image", back_populates="user")

# Table for rating 
class Rating(Base):
    __tablename__ = "rating"
    rating_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.user_id", ondelete="SET NULL"), nullable=False)
    daily_rating = Column(Integer, nullable=True)
    rapid_rating = Column(Integer, nullable=True)
    blitz = Column(Integer, nullable=True)
    bullet_rating = Column(Integer, nullable=True)
    start_timestamp = Column(DateTime, default=datetime.utcnow)
     
    # Defining relationship
    user = relationship("Users", back_populates="ratings")

# class Image(Base):
#     __tablename__ = "image"
#     image_id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("Users.user_id", ondelete="SET NULL"), nullable=False)
#     image_data = Column(LargeBinary, nullable=False)
    
#     # Defining relationship
#     user = relationship("Users", back_populates="images")

Base.metadata.create_all(engine)


session = db  