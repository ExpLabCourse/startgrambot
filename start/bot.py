import config
import telebot

from telebot import types

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    first_button = types.InlineKeyboardButton(text="Темы тестирования", callback_data="first")
    second_button = types.InlineKeyboardButton(text="Дайджест успеха", callback_data="second")
    keyboardmain.add(first_button, second_button)
    bot.send_message(message.chat.id, "Привет, цифровой грамотей!\nДля начала нам необходимо определить твой уровень цифровой грамотности.\nДля этого выбери кнопку \"Темы тестирования\" ", reply_markup=keyboardmain)

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    if call.data == "mainmenu":

        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        first_button = types.InlineKeyboardButton(text="Темы тестирования", callback_data="first")
        second_button = types.InlineKeyboardButton(text="Дайджест успеха", callback_data="second")
        keyboardmain.add(first_button, second_button)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Основное меню",reply_markup=keyboardmain)

    if call.data == "first":
        keyboard = types.InlineKeyboardMarkup()
        rele1 = types.InlineKeyboardButton(text="Коммуникации", callback_data="1")
        rele2 = types.InlineKeyboardButton(text="Создание контента", callback_data="2")
        rele3 = types.InlineKeyboardButton(text="Защита данных", callback_data="3")
        rele4 = types.InlineKeyboardButton(text="Управление данными", callback_data="4")
        rele5 = types.InlineKeyboardButton(text="Решение проблем", callback_data="5")
        backbutton = types.InlineKeyboardButton(text="Назад", callback_data="mainmenu")
        keyboard.add(rele1, rele2, rele3,rele4, rele5, backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Перед тобой 5 тем на выбор.\nНам с тобой необходимо пройти тесирование по всем 5 темам.\nТы самостоятельно определяешь последовательность и темп прохождения тестирования.\nНе переживай, я с тобой!",reply_markup=keyboard)

    elif call.data == "second":
        keyboard = types.InlineKeyboardMarkup()
        rele1 = types.InlineKeyboardButton(text="Мои баллы", callback_data="balls")
        rele2 = types.InlineKeyboardButton(text="Мои сертификаты", callback_data="sert")
        rele3 = types.InlineKeyboardButton(text="Лидерборды", callback_data="lboard")
        backbutton = types.InlineKeyboardButton(text="Назад", callback_data="mainmenu")
        keyboard.add(rele1,rele2, rele3, backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="После прохождения всех тестов, здесь появится твой прогресс",reply_markup=keyboard)

    elif call.data == "1" or call.data == "2" or call.data == "3" or call.data == 4 or call.data == 5:
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Эксперты Цифрового прорыва, тесты готовятся! Возвращайтесь позже...")
        keyboard3 = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="Здесь совсем скоро появятся тесты и все заработает. Пока Вы можете глянуть MVP проекта - @StartgramBot", callback_data="ll")
        keyboard3.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="",reply_markup=keyboard3)


if __name__ == '__main__':
    bot.polling(none_stop=True)