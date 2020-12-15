from loguru import logger

logger.add('tele-bot.log', format='{time} {level} {message}', level='INFO', rotation='10 KB', compression='zip')

BOT_TOKEN = 'YOUR_TOKEN'
