from sqlalchemy import Column, Integer, String
from server.db.db import Base, engine, db
class Users(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, nullable=False)

Base.metadata.create_all(engine)


session = db  
# Example of adding a user to the database

new_user = Users(
    name="Ishaque",
    email ="ishaqueNizamai@gmail.com",
    password="Nizamani123",
    
)
session.add(new_user)
session.commit()