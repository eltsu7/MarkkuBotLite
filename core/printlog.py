from datetime import datetime
from telegram import Update


def printlog(update: Update, message_type):
    username = update.message.from_user.username
    time_string = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    print(f"{time_string} @{username} {message_type}", flush=True)

