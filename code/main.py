import telebot
import requests
import config
from bs4 import BeautifulSoup

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
	bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы показывать погоду на неделю. Чтобы узнать какая температура в вашем городе напишите его название например "Харьков"'.format(message.from_user, bot.get_me()),
		parse_mode='html')
	bot.register_next_step_handler(message, weather)
	
	
@bot.message_handler(content_types=['text'])
def weather(message):
	def get_html(url):
		r = requests.get(url)
		return r.text


	def get_page_data(html):
		soup = BeautifulSoup(html, 'lxml')
		table_month = soup.find('div', class_='tabs').find_all('div', class_='main')
		res = ''
		for i in table_month:
			tempMax = i.find('div', class_='max').find('span').text
			tempMin = i.find('div', class_='min').find('span').text
			dayOfWeek = i.find('p').text
			date = i.find('p', class_='date').text
			month = i.find('p', class_='month').text
			res += dayOfWeek + ' ' + date + ' ' + month +'\n'+ tempMax +'\n'+ tempMin + '\n--------------------\n'
		bot.send_message(message.chat.id, res, parse_mode='html')
			
			
	def main():
		try:
			messages = str(message.text).lower().strip()
			url = f'https://sinoptik.ua/погода-{messages}'
			print(url)
			get_page_data(get_html(url))
		except:
			bot.send_message(message.chat.id, f'Город <b>"{messages}"</b> не найден.', parse_mode='html')
			
	if __name__ == '__main__':
		main()
	
			
bot.polling(none_stop=True)