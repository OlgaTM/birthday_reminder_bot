import json
import logging

import settings

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from db import db_session
from models import User
from crud import create_user, get_all_friends, get_friend
from anketa import (
    anketa_date_of_birth, anketa_friend_profile, anketa_friend_reminder_rule, anketa_hobbies, anketa_start_add_group, anketa_group_name, anketa_group_reminder_rule,
    anketa_start_add_friend, anketa_friend_name, anketa_date_of_birth, anketa_phone_number, anketa_friend_profile, anketa_hobbies, anketa_friend_reminder_rule
)

logging.basicConfig(filename='bot.log', level=logging.INFO)


def greet_user(update, context):
    print ('Вызван /start')
    main_keyboard = ReplyKeyboardMarkup (
        [['Добавить', 'Изменить данные', 'Получить данные', 'Удалить'],
        ['Как работает бот?']],
        resize_keyboard=True
    )
    user_id = update.message.from_user.id
    if not db_session.query(User).filter_by(tg_id = user_id).one():
        update.message.reply_text (
            "Привет, это BirthdayReminderBot, который поможет тебе не забывать о днях рождениях твоих друзей и близких! Выбери любое действие на клавиатуре, чтобы начать.",
            reply_markup = main_keyboard
        )    
        create_user(update.message.from_user)
    else:
        update.message.reply_text (
            f'Привет, {update.message.from_user.first_name}. Выбери любое действие на клавиатуре, чтобы начать.',
            reply_markup = main_keyboard
        )    

def add_data_keyboard(update, context):
    add_keyboard = ReplyKeyboardMarkup(
        [['Нового друга', 'Новую группу'],
        ['Вернуться в главное меню']],
        resize_keyboard=True
    )
    update.message.reply_text(
        "Кого вы хотите добавить?",
        reply_markup = add_keyboard
    )


def change_data_keyboard(update, context):
    change_keyboard = ReplyKeyboardMarkup(
        [['О друге', 'О группе'],
        ['Вернуться в главное меню']], 
        resize_keyboard=True
    )
    update.message.reply_text(
        "Какие данные будем менять?",
        reply_markup = change_keyboard
    )


def change_friend_data(update, context):
    #изменение через анкету делать?
    pass


def change_group_data(update, context):
    pass


def get_data_keyboard(update, context):
    get_keyboard = ReplyKeyboardMarkup(
        [['О моем друге', 'О моей группе'],
        ['О всех моих друзьях', 'О всех моих группах'],
        ['Вернуться в главное меню']],
        resize_keyboard=True
    )
    update.message.reply_text(
        "Какие данные вам отправить?",
        reply_markup = get_keyboard
    )


def get_my_friend_data(update, context):
    update.message.reply_text(
        "Напишите имя вашего друга",
        reply_markup = ReplyKeyboardRemove()
    )
    my_friend_name = update.message.text
    get_friend(
        update.message.from_user.username, 
        my_friend_name
    )
    

def get_my_group_data(update, context):
    pass


def get_all_my_friends_data(update, context):
    json_str = json.dumps(get_all_friends(update.message.from_user.username))
    update.message.reply_text(json_str)
    #Возвращает null


def get_all_my_groups_data(update, context):
    pass


def delete_data_keyboard(update, context):
    delete_keyboard = ReplyKeyboardMarkup(
        [['Друга', 'Группу'],
        ['Вернуться в главное меню']],
        resize_keyboard=True
    )
    update.message.reply_text(
        "Без проблем. Кого удаляем?",
        reply_markup = delete_keyboard
    )


def main_menu_keyboard(update, context):
    menu_keyboard = ReplyKeyboardMarkup (
        [['Добавить', 'Изменить данные', 'Получить данные', 'Удалить'],
        ['Как работает бот?']],
        resize_keyboard=True
    )
    update.message.reply_text (
        "Вы вернулись в главное меню", 
        reply_markup = menu_keyboard
    )   


def main():
    mybot = Updater(settings.API_KEY, use_context = True)
    
    dp = mybot.dispatcher

    anketa_for_groups = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Новую группу)$'), anketa_start_add_group)
        ],
        states={
            "group_name":[MessageHandler(Filters.text, anketa_group_name)],
            "group_reminder_rule":[MessageHandler(Filters.text, anketa_group_reminder_rule)],
        },
        fallbacks=[]
    )

    anketa_for_friends = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Нового друга)$'), anketa_start_add_friend)
        ],
        states={
            "friend_name":[MessageHandler(Filters.text, anketa_friend_name)],
            "date_of_birth":[MessageHandler(Filters.text, anketa_date_of_birth)],
            "phone_number":[MessageHandler(Filters.text, anketa_phone_number)],
            "friend_profile":[MessageHandler(Filters.text, anketa_friend_profile)],
            "hobbies":[MessageHandler(Filters.text, anketa_hobbies)],
            "friend_reminder_rule":[MessageHandler(Filters.text, anketa_friend_reminder_rule)]
        },
        fallbacks=[]
    )

    dp.add_handler(anketa_for_groups)
    dp.add_handler(anketa_for_friends)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Добавить)$'), add_data_keyboard))
    dp.add_handler(MessageHandler(Filters.regex('^(Изменить данные)$'), change_data_keyboard))
    dp.add_handler(MessageHandler(Filters.regex('^(Получить данные)$'), get_data_keyboard))
    dp.add_handler(MessageHandler(Filters.regex('^(Удалить)$'), delete_data_keyboard))
    dp.add_handler(MessageHandler(Filters.regex('^(Вернуться в главное меню)$'), main_menu_keyboard))
    dp.add_handler(MessageHandler(Filters.regex('^(О моем друге)$'), get_my_friend_data))
    dp.add_handler(MessageHandler(Filters.regex('^(О всех моих друзьях)$'), get_all_my_friends_data))
    

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()
    

if __name__ == "__main__":
    main()
