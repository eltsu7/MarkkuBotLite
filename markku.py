# coding: utf-8

from os import environ
from environs import Env

from telegram.ext import ApplicationBuilder, CommandHandler

from commands import start, darkroom


if __name__ == '__main__':
    env = Env()
    env.read_env()

    application = ApplicationBuilder().token(environ["TG_TOKEN"]).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('darkroom', darkroom))

    application.run_polling()
