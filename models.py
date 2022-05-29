import datetime
from db import Base
from sqlalchemy import Float, Integer, Column, String, LargeBinary
import bcrypt

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String)
    password = Column(LargeBinary)

    def verify_password(self, password:str):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

        
class Trascrizione(Base): 
    __tablename__ = "Trascrizione"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    audio = Column(String)
    trascrizione = Column(String)
    data = Column(String)