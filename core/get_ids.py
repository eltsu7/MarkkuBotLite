from telegram import Update

def get_ids(update: Update):
    return update.message.from_user.id, update.message.chat.id
