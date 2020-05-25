import requests
import json
import telebot
import flag
import config

bot = telebot.TeleBot(config.API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'I was by made by MHamidov for getting coronavirus statistics by countries. All you need to do is just to send me country name you want to get statistics. If you want to get worldwide statistics just send `all`')

@bot.message_handler(content_types=['text'])
def send_text_message(message):
    if message.text.upper() == 'ALL':
        response = requests.get('https://corona.lmao.ninja/v2/all')
    else:
        response = requests.get('https://corona.lmao.ninja/v2/countries/' + message.text)

    if response.status_code == 200:
        content = json.loads(response.text)
        country_info = '🌎 *Worldwide*' if message.text.upper() == 'ALL' else flag.flag(content["countryInfo"]["iso2"]) + ' *' + content["country"] + '* '
        bot.send_message(
            message.chat.id, 
            country_info + '\n' +
            '_Total cases:_ *' + str(content["cases"]) + '* 😷\n' +
            '_Cases today:_ *' + str(content["todayCases"]) + '* 🚑\n' +
            '_Active:_ *' + str(content["active"]) + ' 🤒*\n' +
            '_Critical:_ *' + str(content["critical"]) + ' 🤢*\n' +
            '_Total deaths:_ *' + str(content["deaths"]) + ' ⚰*\n' +
            '_Deaths today:_ *' + str(content["todayDeaths"]) + ' ⚰*\n' +
            '_Total recovered:_ *' + str(content["recovered"]) + '* 💊\n',
            parse_mode= 'Markdown'
        )
    else:
        bot.send_message(message.chat.id, 'Country not found')

bot.polling()