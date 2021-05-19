from telegram import Bot
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from echo.config import TG_TOKEN, TG_API_URL
from handlers import do_start, do_echo
from button_handlers import button_request_errors_handler,\
    button_help_handler,\
    button_request_status_handler, \
    button_request_rtp_handler, \
    button_request_vf_handler
import urllib3

def main():
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_API_URL,
    )

    updater = Updater(
        bot=bot,
    )

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", do_start))
    dp.add_handler(CommandHandler("help", button_help_handler))
    dp.add_handler(CommandHandler("request", button_request_errors_handler))
    dp.add_handler(CommandHandler("request_etl", button_request_status_handler))
    dp.add_handler(CommandHandler("request_rtp", button_request_rtp_handler))
    dp.add_handler(CommandHandler("request_vf", button_request_vf_handler))
    dp.add_handler(MessageHandler(Filters.text, do_echo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print('Бот запущен')
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    import requests

    # requests.get('https://api.telegram.org/bot1819897875:AAFybj5a677adMYh9AP6O5Av7AN887WsjHY/sendMessage?chat_id=196673667&text=privet%20ti%20pidor')

    # c = pycurl.Curl()
    # c.setopt(c.URL, 'https://api.telegram.org/bot1819897875:AAFybj5a677adMYh9AP6O5Av7AN887WsjHY/sendMessage?chat_id=196673667&text=privet%20ti%20pidor')

    r = requests.get('https://api.telegram.org/bot1819897875:AAFybj5a677adMYh9AP6O5Av7AN887WsjHY/sendMessage?chat_id=-560181672&text=privet%20ti%20pidor',verify=False)
    main()
