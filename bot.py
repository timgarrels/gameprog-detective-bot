"""Bot Component of the Gameprog Seminar Project 'Detective Game'"""

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
import os
import subprocess
from datetime import datetime

from bot import server_interaction
from bot import telegram_interaction
from bot import SERVER_URL, BOT_TOKEN

def main():
    """Creates a running bot instance with basic game message handlers"""
    # Basic Bot Communication setup
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register /start command handler
    start_handler = CommandHandler('start', telegram_interaction.start_command_callback)
    dispatcher.add_handler(start_handler)

    # Register /describe command handler
    describe_handler = CommandHandler('describe', telegram_interaction.send_current_description)
    dispatcher.add_handler(describe_handler)

    # Register all purpose text handler
    text_handler = MessageHandler(Filters.all, telegram_interaction.reply)
    dispatcher.add_handler(text_handler)

    # Start Bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()