import requests
from bs4 import BeautifulSoup as BS
import webbrowser
import telebot
from telebot import types
bot = telebot.TeleBot('2038959829:AAHVzVx2r7LwkfhwSugZ3WTWMhdF6n9-jtk')
def pars():
    url = requests.get("https://ru.wikipedia.org/wiki/Special:Random")
    soup = BS(url.content, "html.parser")
    
    title = soup.find(class_="firstHeading").text
    link = f'https://ru.wikipedia.org/wiki/{title}'
    return title, link
@bot.message_handler(commands=['start'])
def start(message):
    glav_markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("Прислать ссылку!", callback_data='url')
    btn2 = types.InlineKeyboardButton('Связаться с разработчиком', callback_data='developer')
    glav_markup.add(btn1, btn2)
    bot.send_photo(message.chat.id, photo=open('python.webp', 'rb'))
    bot.send_message(message.chat.id,
    'Привет! Я бот написанный юным красавчиком) при нажатии на кнопку я вышлю вам абсолютно рандомную ссылку из всех википедий которые существуют',
    reply_markup=glav_markup)
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    bot.answer_callback_query(callback_query_id=call.id, text='Спасибо!')
    if call.data == 'url':
        glav_markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("Прислать ссылку еще раз!", callback_data='url')
        glav_markup.add(btn1)
        url = requests.get("https://ru.wikipedia.org/wiki/Special:Random")
        soup = BS(url.content, "html.parser")
        
        title = soup.find(class_="firstHeading").text
        link = f'https://ru.wikipedia.org/wiki/{title}'
        bot.send_message(call.message.chat.id, f'<a href="{link}">{title}</a>', parse_mode='html', reply_markup=glav_markup)
    if call.data == 'developer':
        msg = bot.send_message(call.message.chat.id, 'Отправьте свое сообщение')
        bot.register_next_step_handler(msg, sms)
def sms(message):
    
    bot.send_message(1134632256, f'Вам сообщение от пользователя\n{message.text}\nid: {message.chat.id}')
bot.polling(none_stop=True)