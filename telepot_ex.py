import telepot
from pprint import pprint

token = "283346046:AAECp_TRKwCUJ1E6Xf9sVSBRHtDVzM7aHjE"
dodo = 118931446
shin = 247335685
bot = telepot.Bot(token)
# print(bot.getMe())
# print(bot.getUpdates())

def mimic(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        bot.sendMessage(chat_id, msg['text'])

# bot.message_loop(mimic)
