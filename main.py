import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State
import random
import json

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6677658461:AAGidvZVn50uh4To31dVWcrFA6ILI_rCdto",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()
    num = State()
    bot_age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Регистрация"
text_button_1 = "Рандомное число"
text_button_2 = "Показать кота?"
text_button_3 = "Лотерея"

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Что будем делать?',
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! *Ваше* _имя_?')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! *Ваш* *возраст?*')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Успешная регистрация!', reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    msg = bot.send_message(message.chat.id, "Отправьте число, до которого мы будем у нас будет ограничение",
                           reply_markup=menu_keyboard)
    bot.set_state(message.from_user.id, PollState.num, message.chat.id)


@bot.message_handler(state=PollState.num)
def random_number(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['num'] = message.text
        bot.send_message(message.chat.id, f'Случайное число - {random.randint(1, int(message.text))}')
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    img = 'https://rabotatam.ru/uploads/monthly_2017_04/large.58f1bdeda1c5c_.jpg.91c33c120ad86a4dbf2c50dd44d00890.jpg'
    bot.send_photo(message.chat.id, photo=img, reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Угадайте мой возраст!", reply_markup=menu_keyboard)
    bot.set_state(message.from_user.id, PollState.bot_age, message.chat.id)


@bot.message_handler(state=PollState.bot_age)
def fortuna(message):
    if int(message.text) == 985:
        bot.send_message(message.chat.id, 'Вы угадали, мне 985 лет')
    else:
        bot.send_message(message.chat.id, 'К сожалению, вы не угадали мой возраст :(')
    bot.set_state(message.from_user.id, PollState.bot_age, message.chat.id)

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()
