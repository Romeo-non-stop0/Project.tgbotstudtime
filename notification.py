import telebot
from telebot import types
from notifiers import notify
import threading

TOKEN = '7830171145:AAEOU0N9FDRUbehoUpo_4GZYFsTPuFRKtlc'
bot = telebot.TeleBot(TOKEN)

notifications = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    item = types.KeyboardButton("Уведомления")
    markup.add(item)
    bot.send_message(message.chat.id, "Привет! Нажмите кнопку, чтобы добавить уведомление.", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == "Уведомления")
def handle_notifications(message):
    msg = bot.send_message(message.chat.id, "Введите количество минут до напоминания:")
    bot.register_next_step_handler(msg, process_minutes)

def process_minutes(message):
    try:
        minutes = int(message.text)
        if minutes < 1:
            raise ValueError("Количество минут должно быть положительным.")
        notifications[message.chat.id] = {'minutes': minutes}
        msg = bot.send_message(message.chat.id, "Введите название для дедлайна:")
        bot.register_next_step_handler(msg, process_deadline, minutes)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное количество минут.")
        msg = bot.send_message(message.chat.id, "Введите количество минут до напоминания:")
        bot.register_next_step_handler(msg, process_minutes)
def process_deadline(message, minutes):
    deadline_name = message.text
    notifications[message.chat.id]['name'] = deadline_name
    # Устанавливаем время напоминания
    bot.send_message(message.chat.id, f"Уведомление для '{deadline_name}' установлено на {minutes} минут.")
    # Запускаем таймер для отправки уведомления
    threading.Timer(minutes * 60, send_notification, args=(message.chat.id, deadline_name)).start()

def send_notification(chat_id, deadline_name):
    # Отправка уведомления пользователю
    bot.send_message(chat_id, f'Не забудьте о дедлайне: {deadline_name}')
    # notify.send('Deadline Reminder', message=f'Не забудьте о дедлайне: {deadline_name}')     # Отправка уведомления с помощью notifiers

bot.polling(none_stop=True)
