import telebot
import pandas as pd
bot = telebot.TeleBot('1240479598:AAFa87oq_hfSjcxFrJ2XvXuYLh5DUAvA0p8')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True,True,True)
keyboard1.row('Топ 10 популярных фильмов', 'Поиск фильма')

keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True, True)
keyboard2.row('Жанр', 'Год выпуска', 'Рейтинг')

df1 = pd.read_csv(r'C:\Users\alimb\PycharmProjects\CinemaBot\IMDb movies.csv')
df2 = pd.read_csv(r'C:\Users\alimb\PycharmProjects\CinemaBot\IMDb ratings.csv')
df = pd.merge(df1,df2,on='imdb_title_id')
df = df[df['votes']>200000]
top_10 = df.sort_values(by=['weighted_average_vote'],ascending=False)[0:10]
# top_10[['title','genre','year','weighted_average_vote']]
c = [(x,y) for x,y in zip(list(top_10['title']),list(top_10['imdb_title_id']))]

@bot.message_handler(commands=['start'])
def start_message(message):
    print(message)
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message)
    if message.text.lower() == 'поиск фильма':
        bot.send_message(message.chat.id, "Выбери параметры фильма.", reply_markup=keyboard2)
    elif message.text.lower() == 'топ 10 популярных фильмов':
        keyboard = telebot.types.InlineKeyboardMarkup()
        for i,j in c:
            key = telebot.types.InlineKeyboardButton(text=i, url='https://www.imdb.com/title/{}/'.format(j))
            keyboard.add(key)
        bot.send_message(message.from_user.id, text='Можешь фильмец выбрать, вот 10 лучших:', reply_markup=keyboard)

bot.polling(none_stop=True, interval=0)
# orkrgmkvg