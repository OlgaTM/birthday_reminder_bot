from datetime import date
from enum import unique
from sqlalchemy import Column, Integer, String, Date, ForeignKey

from db import Base, engine


class User(Base):
    __tablename__ = "users"

    tg_id = Column(Integer, primary_key=True, nullable = False)
    name = Column(String(), nullable = False)
    login = Column(String(), unique=True, nullable = False)
    password = Column(String(), nullable = False)

    def __repr__(self):
        return f"User_tg_id {self.tg_id}, Имя {self.name}, login {self.login}, password {self.password}"

#class Group(Base):
    #__tablename__ = "groups"

    #id = Column(Integer, primary_key=True)
    #user_id = Column(Integer, ForeignKey(User.id), index = True, nullable = False)
    #name = Column(String, unique = True, nullable = False)
    #reminder_rule = Column(Integer)

    #def __repr__(self):
        #return f"Group {self.id}, {self.name}, {self.reminder_rule}"

class People(Base):
    __tablename__ = "peoples"

    user_login = Column(String, ForeignKey(User.login), index = True, nullable = False)
    #group_id = Column(Integer, ForeignKey(Group.id), index = True, nullable = False)
    name = Column(String, primary_key=True, nullable = False)
    date_of_birth = Column(Date, nullable = False)
    phone = Column(String)
    profile = Column(String)
    hobbies = Column(String)
    reminder_rule = Column(Integer)

    def __repr__(self):
        return f"Person {self.user_tg_id}, {self.name}, {self.date_of_birth}, {self.reminder_rule}"

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
