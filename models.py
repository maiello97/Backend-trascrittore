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

        