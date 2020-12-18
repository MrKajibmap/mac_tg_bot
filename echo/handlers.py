from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup

from echo.config import button_help_text, \
    button_request_errors_text, \
    button_request_status_text, \
    button_request_rtp_text, \
    button_request_vf_text
from button_handlers import button_help_handler, \
    button_request_errors_handler, \
    button_request_status_handler, \
    button_request_rtp_handler, \
    button_request_vf_handler

reply_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=button_help_text),
            KeyboardButton(text=button_request_errors_text),
            KeyboardButton(text=button_request_status_text),
            KeyboardButton(text=button_request_rtp_text),
            KeyboardButton(text=button_request_vf_text),
        ],
    ],
    resize_keyboard=True,
)


def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Ну че, народ, погнали?!",
        reply_markup=reply_markup
    )


def do_echo(bot: Bot, update: Update):
    response = update.message.text
    if response == "волк":
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Красавчик',
            reply_markup=reply_markup
        )
        bot.send_photo(
            chat_id=update.message.chat_id,
            photo='https://sivator.com/uploads/posts/2017-08/1502205903_1502173813-b069a578be0f92e8aa2530d369e3b944.jpeg'
        )
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Похоже на вызов запроса...',
            reply_markup=reply_markup
        )

    if response == button_help_text:
        return button_help_handler(bot=bot, update=update)
    elif response == button_request_errors_text:
        return button_request_errors_handler(bot, update)
    elif response == button_request_status_text:
        return button_request_status_handler(bot, update)
    elif response == button_request_rtp_text:
        return button_request_rtp_handler(bot, update)
    elif response == button_request_vf_text:
        return button_request_vf_handler(bot, update)
