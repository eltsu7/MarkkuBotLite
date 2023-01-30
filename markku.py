# coding: utf-8

from os import environ
from environs import Env

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    BaseFilter,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
    CallbackQueryHandler,
)

from command_router import CommandRouter


def handlers(updater):
    dp = updater.dispatcher

    # Alustetaan routerit
    cr = CommandRouter()

    # Komennot
    dp.add_handler(CommandHandler(cr.get_commands(), cr.route_command, pass_args=True))


def main():
    env = Env()
    env.read_env()

    updater = Updater(token=environ["TG_TOKEN"])
    handlers(updater)

    updater.start_polling()


main()
