import telebot
from telebot import types

from config import token, admin_ids, channel_id, admin_chat_id

bot = telebot.TeleBot(token)

admin_ids = admin_ids
admin_chat_id = admin_chat_id

channel_id = channel_id  # Замените на фактический ID вашего канала

user_messages = []  # Хранение сообщений от пользователей
pending_messages = {}
# Флаг для отслеживания состояния автопостинга
autoposting_enabled = False

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.from_user.id in admin_ids:
        btn1 = types.KeyboardButton('💫 Панель администратора 💫')
        markup.add(btn1)
        bot.send_message(message.chat.id, "Панель администратора", reply_markup=markup)
    else:
        btn1 = types.KeyboardButton('👀 Предложить идею')
        btn2 = types.KeyboardButton('☎️ Помощь')
        btn3 = types.KeyboardButton('🥖 Донат на пирожок')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, "Привет", reply_markup=markup)

# Добавленная функция для обработки сообщений пользователей
@bot.message_handler(func=lambda message: True)
def handle_user(message):
    # print(pending_messages)
    # print("Received text message:", message.text)
    if message.from_user.id in admin_ids:
        handle_admin(message)
    else:
        # print(message.text)
        if message.text == '👀 Предложить идею':
            bot.send_message(message.chat.id, "Предложи свой пост, если модерация одобрит его, его отправят в канал:)")
            bot.send_message(message.chat.id, "Введите текст")
            pending_messages[message.chat.id] = 'Введите текст'

        elif message.text == '☎️ Помощь':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('❓ Как предложить идею')
            btn2 = types.KeyboardButton('🥴 Что делать если я забанен')
            btn3 = types.KeyboardButton('🤝 Другой вопрос')
            btn4 = types.KeyboardButton('Выход')
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, "Помощь", reply_markup=markup)

        elif message.text == '❓ Как предложить идею':
            bot.send_message(message.chat.id, "Как предложить идею: чтобы предложить идею, зайдите в бота, снизу появятся две кнопки, одна из них будет 'Предложить идею'. Нажмите на нее и пишите текст, который мы в скором времени выложим :)")

        elif message.text == '🥴 Что делать если я забанен':
            bot.send_message(message.chat.id, "Если вы забанены, ничего сделать нельзя, так как вы нарушили правила канала!")

        elif message.text == '🤝 Другой вопрос':
            bot.send_message(message.chat.id, "В описании профиля, перейдите на вторую ссылку в анонимном боте.")

        elif message.text == 'Выход':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('👀 Предложить идею')
            btn2 = types.KeyboardButton('☎️ Помощь')
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, "Выход", reply_markup=markup)

        elif message.text == '🥖 Донат на пирожок':
            bot.send_message(message.chat.id, "Донат на пирожок для потдержки адмиина можно прислать на карту сбер")
            bot.send_message(message.chat.id, "С сообщением которое вы хотите опубликовать")
            bot.send_message(message.chat.id, "2202 2009 6688 8685")

        # elif message.text == 'Введите текст':
        elif pending_messages.get(message.chat.id) == 'Введите текст':
            # print(pending_messages)
            if autoposting_enabled:
                # Если включен автопостинг, публикуем сообщение сразу
                bot.send_message(channel_id, message.text)
                bot.send_message(message.chat.id, "Сообщение опубликовано в канале.")
                bot.send_message(message.chat.id, "Выход.")

                pending_messages.pop(message.chat.id, None)
            else:
                user_messages.append({
                    'id': message.from_user.id,
                    'name': message.from_user.username,
                    'text': message.text
                })
                bot.send_message(message.chat.id, "Сообщение отправлено на модерацию.")
                bot.send_message(message.chat.id, "Выход.")


        else:
            bot.send_message(message.chat.id, "Нажмите на 👀 Предложить идею")
            bot.send_message(message.chat.id, "Введите текст и отправить.")



@bot.message_handler(func=lambda message: message.from_user.id in admin_ids)
def handle_admin(message):
    global autoposting_enabled
    # print(autoposting_enabled)
    if message.text == '💫 Панель администратора 💫':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('👩‍🎤 Автопостинг')
        btn2 = types.KeyboardButton('👩‍🔧 Стандартный-мод')

        btn3 = types.KeyboardButton('Выход')
        btn4 = types.KeyboardButton('👀 Посмотреть сообщения от пользователей')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Какое действие выполнить?", reply_markup=markup)
        if autoposting_enabled:
            bot.send_message(message.chat.id, "Автопостинг включен", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Стандартный-мод включен ", reply_markup=markup)

    elif message.text == '👀 Посмотреть сообщения от пользователей':
        view_admin_messages(message)

    elif message.text == '👩‍🎤 Автопостинг':
        autoposting_enabled = True
        bot.send_message(message.chat.id, "Автопостинг включен")

    elif message.text == '👩‍🔧 Стандартный-мод':
        autoposting_enabled = False
        bot.send_message(message.chat.id, "Стандартный-мод включен")

    elif message.text == 'Выход':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('💫 Панель администратора 💫')
        markup.add(btn1)
        bot.send_message(message.chat.id, "Админ панель", reply_markup=markup)

def view_admin_messages(message):
    if user_messages:
        for user_message in user_messages:
            markup = types.InlineKeyboardMarkup()

            # Отправить первое сообщение с кнопкой "Заблокировать"
            # btn_block = types.InlineKeyboardButton("Заблокировать", callback_data=f"block_{user_message['id']}")
            # markup.row(btn_block)
            bot.send_message(
                message.chat.id,
                f"Сообщение от @{user_message['name']} :\n{user_message['text']}",
                reply_markup=markup
            )

            # Отправить второе сообщение с кнопками "Опубликовать" и "Отменить"
            markup = types.InlineKeyboardMarkup()
            btn_publish = types.InlineKeyboardButton("Опубликовать", callback_data=f"publish_{user_message['id']}")
            btn_cancel = types.InlineKeyboardButton("Отменить", callback_data=f"cancel_{user_message['id']}")
            markup.row(btn_publish, btn_cancel)
            bot.send_message(
                message.chat.id,
                user_message['text'],
                reply_markup=markup
            )

    else:
        bot.send_message(message.chat.id, "Нет сообщений от пользователей для обработки.")


@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    # Извлекаем данные из callback_data
    action, user_id = call.data.split('_') # cancel и id-пользователя
    user_text = call.message.text  # текст выбранного сообщения


    if action == "block":
        pass
    elif action == "publish":
        bot.send_message(channel_id, user_text)

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        prev_user_message = next(
            (msg for msg in user_messages if msg.get('id') == int(user_id) and msg.get('text') == user_text), None)
        if prev_user_message:
            user_messages.remove(prev_user_message)

        bot.send_message(call.message.chat.id, "Сообщение отправлено.")
    elif action == "cancel":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        prev_user_message = next(
            (msg for msg in user_messages if msg.get('id') == int(user_id) and msg.get('text') == user_text), None)
        if prev_user_message:
            user_messages.remove(prev_user_message)

        bot.send_message(call.message.chat.id, "Сообщение отклонено.")


if __name__ == '__main__':
    bot.delete_webhook()
    bot.polling(none_stop=True)
