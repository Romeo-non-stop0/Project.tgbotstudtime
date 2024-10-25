# Импортируем библиотеки пайтон
import telebot
import datetime
import time
from telebot import types
from notifiers import get_notifier, notify
import threading

bot = telebot.TeleBot('7830171145:AAEOU0N9FDRUbehoUpo_4GZYFsTPuFRKtlc')

notifications = {}
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет, я бот с расписанием занятий! Выберите действие:", reply_markup=keyboard)

# Создание клавиатуры с кнопками
keyboard = types.ReplyKeyboardMarkup(row_width=1)
button1 = types.KeyboardButton("Расписание")
button2 = types.KeyboardButton("Дедлайны")
button3 = types.KeyboardButton("Каникулы и сессии")
button4 = types.KeyboardButton("Включить уведомления на дедлайны")
keyboard.add(button1, button2, button3, button4)

# Обработка нажатий на кнопки
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "Расписание":
        bot.send_message(message.chat.id, "Джага Джага")
        bot.send_message(message.chat.id, datetime.datetime.now().strftime("%A"))
       # bot.reply_to(message, format_schedule(get_today_schedule()))
    elif message.text == "Дедлайны":
        bot.reply_to(message, "ggg(")

    elif message.text == "Каникулы и сессии":
        bot.reply_to(message, "тут пока ничего нет(")
    elif message.text == "Включить уведомления на дедлайны":
        handle_notifications(message)

# Список с расписанием занятий, Чётная = Schedule 2, Нечётная  Schedule 1
schedule1 = {
    'Tuesday': [
        {'Время': '9:30 - 10:50', 'Предмет': 'БП-126, лекция, Дискретная математика (Мокеев Д.Б.'},
        {'Время': '11:10 - 12:30', 'Предмет': 'БП-405, семинар, Электроснабжение железных дорог (Цаплина Е.К.)'},
        {'Время': '13:00 - 14:20', 'Предмет': 'БП-406, семинар, Математический анализ (Чистякова С.А.)'},
    ],
    'Wednesday': [
        {'Время': '9:30 - 10:50', 'Предмет': 'Л-318, семинар, Линейная алгебра и геометрия (Беспалов П.А.)'},
        {'Время': '11:10 - 12:30', 'Предмет': 'Л-323, лекция, Программирование С/С++ (Пеплин Ф.С.)'},
        {'Время': '13:00 - 14:20', 'Предмет': 'Л-225, лекция, Линейная алгебра и геометрия (Савина О.Н.)'},
        {'Время': '14:40 - 16:00', 'Предмет': 'БП-406, семинар, Математический анализ (Чистяков В.В.)'},
    ],
    'Friday': [
        {'Время': '13:00 - 14:20', 'Предмет': 'online, семинар, Основы Российской Государственности (Константинова Т.Н.)'},
        {'Время': '14:40 - 16:00', 'Предмет': 'online, семинар, История России (Константинова Т.Н.)'},
    ],
    'Saturday':[
        {'Время': '8:00 - 9:20', 'Предмет': 'Л-325, Английский язык (Черницкая М.Б.)'},
        {'Время': '9:30 - 10:50', 'Предмет': 'Л-325, Английский язык (Черницкая М.Б.)'}
    ]
}

schedule2 = {
    'Monday': [
        {'Время': '11:10 - 12:30', 'Предмет': 'БП-216, практика, Программирование на С++'},
        {'Время': '13:00 - 14:20', 'Предмет': 'БП-216, практика, Программирование на С++'},
    ],
    'Tuesday': [
        {'Время': '9:30 - 10:50', 'Предмет': 'БП-126, лекция, Дискретная математика (Мокеев Д.Б.'},
        {'Время': '11:10 - 12:30', 'Предмет': 'БП-405, семинар, Электроснабжение железных дорог (Цаплина Е.К.)'},
        {'Время': '13:00 - 14:20', 'Предмет': 'БП-406, семинар, Математический анализ (Чистякова С.А.)'},
    ],
    'Wednesday': [
        {'Время': '9:30 - 10:50', 'Предмет': 'Л-318, семинар, Линейная алгебра и геометрия (Беспалов П.А.)'},
        {'Время': '11:10 - 12:30', 'Предмет': 'Л-323, лекция, Программирование С/С++ (Пеплин Ф.С.)'},
        {'Время': '13:00 - 14:20', 'Предмет': 'Л-225, лекция, Линейная алгебра и геометрия (Савина О.Н.)'},
        {'Время': '14:40 - 16:00', 'Предмет': 'БП-406, семинар, Математический анализ (Чистяков В.В.)'},
    ],
    'Friday': [
        {'Время': '13:00 - 14:20', 'Предмет': 'online, семинар, Основы Российской Государственности (Константинова Т.Н.)'},
        {'Время': '14:40 - 16:00', 'Предмет': 'online, семинар, История России (Константинова Т.Н.)'},
    ],
    'Saturday':[
        {'Время': '8:00 - 9:20', 'Предмет': 'Л-325, Английский язык (Черницкая М.Б.)'},
        {'Время': '9:30 - 10:50', 'Предмет': 'Л-325, Английский язык (Черницкая М.Б.)'}
    ]
}
now = datetime.datetime.now()        # Получаем текущую дату с помощью библиотеки datetime
week_number = now.isocalendar()[1]   # Получаем номер недели в году с помощью библиотеки datetime

# Функция для получения расписания на текущий день
def get_today_schedule():
    current_day = datetime.datetime.now().strftime("%A")
    if week_number % 2 == 0 and current_day in schedule2:
        return schedule2[current_day]
    elif current_day in schedule1:
        return schedule1[current_day]
    else:
        return []

# Функция для форматированного вывода расписания в текстовом формате
def format_schedule(schedule):
    if not schedule:
        return "Сегодня пар нет!"
    else:
        result = "Расписание на сегодня:\n"
        for lesson in schedule:
            result += f"{lesson['Время']} - {lesson['Предмет']}\n"
        return result


#Уведомления
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

bot.polling(none_stop=True, interval=0)   # Запускаем бота

#В этом примере бот отвечает на команду /schedule отправкой расписания занятий на текущий день в чат.