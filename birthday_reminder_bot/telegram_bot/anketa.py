from telegram import ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from crud import add_friend


def anketa_start_add_group(update, context):
    update.message.reply_text(
        "Напишите название новой группы",
        reply_markup = ReplyKeyboardRemove()
    )
    return "group_name"


def anketa_group_name(update, context):
    new_group_name = update.message.text.lower().capitalize()
    if new_group_name in Group.name:
        update.message.reply_text ("Группа с таким названием уже сущетсвует")
    else:
        context.user_data["anketa"]={"group_name": new_group_name}
        reply_keyboard = [
            ["0", "1", "3", "5", "7", "10", "14", "30"]
        ]
        update.message.reply_text(
            f"За сколько дней вам напоминать о днях рождениях людей из группы {new_group_name}?",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True, resize_keyboard=True)
        )
        return "group_reminder_rule"


def anketa_group_reminder_rule(update, context):
    context.user_data["anketa"]["group_reminder_rule"] = int(update.message.text)
    menu_keyboard = ReplyKeyboardMarkup (
        [['Добавить', 'Изменить данные', 'Получить данные', 'Удалить'],
        ['Как работает бот?']],
        resize_keyboard=True
    )
    new_group = f"""
    <b>Название группы:</b> {context.user_data['anketa_for_groups']['group_name']}
    <b>Напоминание:</b> за {context.user_data['anketa_for_groups']['group_reminder_rule']} дней
    """
    update.message.reply_text(
        new_group, reply_markup = menu_keyboard,
        parse_mode = ParseMode.HTML
    )
    return ConversationHandler.END
    

def anketa_start_add_friend(update, context):
    update.message.reply_text(
        "Как зовут вашего друга? Укажите отличительное особенное описание для этого человека или фамилию. Например - Костя Костоправ.",
        reply_markup = ReplyKeyboardRemove()
    )
    return "friend_name"


def anketa_friend_name(update, context):
    new_friend_name = update.message.text.lower().capitalize()
    if len(new_friend_name.split(' ')) < 2:
        update.message.reply_text("Напишите не только имя, а еще и отличительную характеристику или Фамилию человка, по которой вы легко сможете его найти и опознать.")
        return "friend_name"
    else:
        context.user_data["anketa_for_friends"]={"friend_name": new_friend_name}
        update.message.reply_text(
            f"Когда день рождения у {new_friend_name}? Введите в формте дд-мм-гггг"
        )
        return "date_of_birth"


def anketa_date_of_birth(update, context):
    birthday = update.message.text
    if len(birthday.split('-')) < 3:
        update.message.reply_text("Введите день, месяц и год рождения в формате дд-мм-гггг, если не известен год рождения укажите 1900")
        return "date_of_birth"
    else:
        context.user_data["anketa_for_friends"]["date_of_birth"] = update.message.text
        reply_keyboard = [["Пропустить"]]
        update.message.reply_text(
            f"Введите номер телефона, если знаете или нажмите 'Пропустить'",
            reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        )
        return "phone_number"


def anketa_phone_number(update, context):
    context.user_data["anketa_for_friends"]["phone_number"] = update.message.text
    update.message.reply_text("Вставьте ссылку на профиль, если знаете или нажмите 'Пропустить'")
    return "friend_profile"


def anketa_friend_profile(update, context):
    context.user_data["anketa_for_friends"]["friend_profile"] = update.message.text
    update.message.reply_text(
        "Введите хобби вашего друга",
        reply_markup = ReplyKeyboardRemove()
    )
    return "hobbies"


def anketa_hobbies(update, context):
    context.user_data["anketa_for_friends"]["hobbies"] = update.message.text
    reply_keyboard = [
            ["0", "1", "3", "5", "7", "10", "14", "30"]
        ]
    update.message.reply_text(
        f"За сколько дней вам напоминать о дне рождении?",
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    )
    return "friend_reminder_rule"


def anketa_friend_reminder_rule(update, context):
    context.user_data["anketa_for_friends"]["friend_reminder_rule"] = int(update.message.text)
    menu_keyboard = ReplyKeyboardMarkup (
        [['Добавить', 'Изменить данные', 'Получить данные', 'Удалить'],
        ['Как работает бот?']],
        resize_keyboard=True
    )

    new_friend = f"""
    <b>Имя:</b> {context.user_data['anketa_for_friends']['friend_name']}
    <b>Дата рождения:</b> {context.user_data['anketa_for_friends']['date_of_birth']}
    <b>Номер телефона:</b> {context.user_data['anketa_for_friends']['phone_number']}
    <b>Профиль:</b> {context.user_data['anketa_for_friends']['friend_profile']}
    <b>Хобби:</b> {context.user_data['anketa_for_friends']['hobbies']}
    <b>Напоминание:</b> за {context.user_data['anketa_for_friends']['friend_reminder_rule']} дней
    """
    update.message.reply_text(
        new_friend, reply_markup = menu_keyboard,
        parse_mode = ParseMode.HTML
    )

    add_friend(
        update.message.from_user.username,
        context.user_data['anketa_for_friends']['friend_name'],
        context.user_data['anketa_for_friends']['date_of_birth'],
        context.user_data['anketa_for_friends']['phone_number'],
        context.user_data['anketa_for_friends']['friend_profile'],
        context.user_data['anketa_for_friends']['hobbies'],
        context.user_data['anketa_for_friends']['friend_reminder_rule']
    )
    
    return ConversationHandler.END
    
