from db import db_session
from models import User, People


def create_user(user):    
    user_one = User(tg_id = user.id, name = user.first_name, login = user.username, password = "1111")

    db_session.add(user_one)
    db_session.commit()

    
def get_user(user):
    my_user = db_session.query(User).filter_by(tg_id = user.id).one()


def get_friend(user_login, friend_name):
    my_friend = db_session.query(People).filter_by(user_login = user_login, name = friend_name).first()
    return ("""
    f'Имя: {my_friend.name},
    Дата рождения: {my_friend.date_of_birth},
    Телефон: {my_friend.phone},
    Профиль: {my_friend.profile},
    Хобби: {my_friend.hobbies}
    """)


def get_all_friends(user_login):
    all_friends = db_session.query(People.name).filter_by(user_login = user_login).all()
    return all_friends   
    
def add_friend(
    user_login,
    friend_name,
    date_of_birth,
    phone_number,
    friend_profile,
    hobbies,
    friend_reminder_rule
):
    friend_one = People(
        user_login = user_login,
        name = friend_name, 
        date_of_birth = date_of_birth, 
        phone = phone_number, 
        profile = friend_profile, 
        hobbies = hobbies, 
        reminder_rule = friend_reminder_rule
        )

    db_session.add(friend_one)
    db_session.commit()
   