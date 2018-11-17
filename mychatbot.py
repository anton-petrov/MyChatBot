# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
import logging

telegram_token = ''
dialogflow_token = ''

with open(".credentials") as file:
    for line in file:
        exec(line)
        
# Токен API к Telegram
updater = Updater(token=telegram_token)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)

#===============================================================================
# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')
#===============================================================================
def textMessage(bot, update):
    # Токен API к Dialogflow
    request = apiai.ApiAI(dialogflow_token).text_request()
    # На каком языке будет послан запрос
    request.lang = 'ru'
    # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.session_id = 'MyChatBotAI'
    # Посылаем запрос к ИИ с сообщением от юзера
    request.query = update.message.text

    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    # parse response from Google AI
    response = responseJson['result']['fulfillment']['speech']

#    response = 'Получил Ваше сообщение: ' + update.message.text

    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Извинте, но я Вас не понял...')
#===============================================================================

# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
