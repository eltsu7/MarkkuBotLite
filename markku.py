# coding: utf-8

from os import environ
from environs import Env

from telegram.ext import ApplicationBuilder, CommandHandler

from commands import start, darkroom
from core.printlog import printlog


if __name__ == '__main__':
    printlog(message="Starting bot")

    env = Env()
    env.read_env()

    application = ApplicationBuilder().token(environ["TG_TOKEN"]).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('darkroom', darkroom))

    printlog(message="Starting to poll")

    application.run_polling()
