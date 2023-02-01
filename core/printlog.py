from datetime import datetime
from telegram import Update


def printlog(update: Update = None, message: str = ""):
    log_message = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    if update:
        log_message += " @" + update.message.from_user.username

    log_message += " " + message

    print(log_message, flush=True)
