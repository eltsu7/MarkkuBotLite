import json

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from urllib.request import urlopen
from urllib.error import URLError
from os import environ
import logging

from core.printlog import printlog
from core.get_ids import get_ids

class SensorEntry:
    def __init__(self, name, value, insert_time):
        self.__name = name
        self.__value = value
        self.__insert_time = insert_time

    def name(self):
        return self.__name

    def value(self):
        return self.__value

    def insert_time(self):
        return self.__insert_time

def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    printlog(update, "/start")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Woof woof!")

def darkroom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    printlog(update, "/darkroom")
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_darkroom_message())

# Lukee netistä valosensorin datan ja kertoo onko kerhohuoneella valot päällä
def get_darkroom_message():
    try:
        with urlopen(environ["SENSOR_API_ADDRESS"]) as url:
            sensor_data = json.loads(url.read().decode())

            # JSON härössä muodossa, sen takia teemme näin. Esimerkki:
            #   {"entries": [{"value": 191, "sensor": "light1", "inserted": "2018-07-27T16:18:43.589Z"}]}

            if len(sensor_data["entries"]) != 0:

                for sensor in sensor_data["entries"]:
                    sensor_entry = handle_sensor(sensor)
                    if sensor_entry.name() == "light1":
                        return get_light_message(sensor_entry)

                return "Can't reach darkroom 🤔"
            else:
                return "🤷‍♂️"

    except URLError as e:
        print(e.reason)
        return f"Ei ny onnistunu ({e.reason})"

def handle_sensor(sensor_data):
    return SensorEntry(
        sensor_data["sensor"], sensor_data["value"], sensor_data["inserted"]
    )

def get_light_message(light_sensor_entry: SensorEntry):
    if light_sensor_entry.value() > 0:
        return "Someone is in the darkroom 😊"

    return "Darkroom is empty ☹️"
