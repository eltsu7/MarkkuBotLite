# -*- coding: utf-8 -*-
import json
from urllib.request import urlopen, Request
from urllib.error import URLError
import random
from os import environ
import time
from datetime import datetime

from core.printlog import printlog
from core.get_ids import get_ids

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


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


class CommandRouter:
    def __init__(self):
        self.last_command = {}

        self.commands = {
            "/start": self.start,
            "/darkroom": self.darkroom,
        }

    def get_commands(self):
        # yllä olevat komennot
        coms = self.commands.keys()

        # poistetaan '/' edestä
        return [x[1:] for x in coms]

    def route_command(self, bot, update, args=[]):
        message = update.message.text.split(" ")[0]

        # poistetaan '@<BotUsername>' komennosta jos löytyy
        if "@" in message:
            message = message.split("@", 1)[0]

        printlog(update, message)

        if message in self.commands:
            self.commands[message](bot, update, args)

    def on_timeout(self, user_id, chat_id):
        current_time = time.time()

        # privassa saa spämmii
        if user_id == chat_id:
            return False

        if (user_id, chat_id) in self.last_command and self.last_command[
            (user_id, chat_id)
        ] + 60 > current_time:
            return True
        else:
            self.last_command[(user_id, chat_id)] = current_time
            return False

    def start(self, bot, update, args):
        _, chat_id = get_ids(update)

        bot.send_message(chat_id=chat_id, text="Woof woof")

    # Lukee netistä valosensorin datan ja kertoo onko kerhohuoneella valot päällä
    def darkroom(self, bot, update, args):
        user_id, chat_id = get_ids(update)

        if self.on_timeout(user_id, chat_id):
            return

        try:
            with urlopen(environ["SENSOR_API_ADDRESS"]) as url:
                sensor_data = json.loads(url.read().decode())

                # JSON härössä muodossa, sen takia teemme näin. Esimerkki:
                #   {"entries": [{"value": 191, "sensor": "light1", "inserted": "2018-07-27T16:18:43.589Z"}]}

                if len(sensor_data["entries"]) != 0:

                    light_message = ""
                    voice_message = ""

                    for sensor in sensor_data["entries"]:
                        sensor_entry = CommandRouter.handle_sensor(sensor)
                        if sensor_entry.name() == "light1":
                            light_message = CommandRouter.get_light_message(
                                sensor_entry
                            )
                        elif sensor_entry.name() == "voice1":
                            voice_message = CommandRouter.get_voice_message(
                                sensor_entry
                            )

                    if not light_message:
                        light_message = "Can't reach darkroom 🤔"
                    if not voice_message:
                        voice_message = "Can't reach virtual darkroom 🤔"

                    reply = f"{light_message}."

                else:
                    reply = "🤷‍♂️"

            bot.send_message(chat_id=chat_id, text=reply)
        except URLError as e:
            print(e.reason)
            bot.send_message(chat_id=chat_id, text="Ei ny onnistunu (%s)" % e.reason)

    @staticmethod
    def handle_sensor(sensor_data):
        return SensorEntry(
            sensor_data["sensor"], sensor_data["value"], sensor_data["inserted"]
        )

    @staticmethod
    def get_light_message(light_sensor_entry):
        if not light_sensor_entry:
            return None

        if light_sensor_entry.value() > 0:
            return "Someone is in the darkroom 😊"

        return "Darkroom is empty ☹️"

    @staticmethod
    def get_voice_message(voice_data):
        if not voice_data:
            return None

        if voice_data.value() > 0:
            return "Somebody is in the virtual darkroom 😊"

        return "Virtual darkroom is empty ☹️"
