from sqlalchemy import Column, Integer, String , Float, ForeignKey 
from sqlalchemy.orm import relationship
from database.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True,nullable=False)
    email = Column(String,index=True,unique=True,nullable=False)
    password = Column(String,nullable=False)
    
class Fund(Base):
    __tablename__ = "funds"

    scheme_code = Column(Integer, primary_key=True, index=True)  
    scheme_name = Column(String, nullable=False)  
    nav = Column(Float, nullable=False)  
    scheme_type = Column(String, nullable=True) 
    scheme_category = Column(String, nullable=True)  
    investments = relationship("Investment", back_populates="fund")
    
class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  
    scheme_code = Column(Integer, ForeignKey("funds.scheme_code")) 
    units = Column(Float, nullable=False)
    total_value = Column(Float, nullable=False)
    fund = relationship("Fund", back_populates="investments")

