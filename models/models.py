from sqlalchemy import Column, Integer, String , Float, ForeignKey 
from database.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True,nullable=False)
    email = Column(String,index=True,unique=True,nullable=False)
    password = Column(String,nullable=False)
    
class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scheme_code = Column(Integer, nullable=False)
    scheme_name = Column(String, nullable=False)
    units = Column(Float, nullable=False) 
    