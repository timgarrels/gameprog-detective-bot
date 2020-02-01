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

    # TODO: For dev purpose only
    # Register /update command handler
    update_handler = CommandHandler('update', update)
    dispatcher.add_handler(update_handler)

    # Register /describe command handler
    describe_handler = CommandHandler('describe', telegram_interaction.send_current_description)
    dispatcher.add_handler(describe_handler)

    # Register all purpose text handler
    text_handler = MessageHandler(Filters.all, telegram_interaction.reply)
    dispatcher.add_handler(text_handler)

    # Start Bot
    updater.start_polling()
    updater.idle()

def update(update, context):
    """Hook to redeploy prod bot via github webhook
    Performs a git pull and a restart of bot"""
    FNULL = open(os.devnull, 'w')
    try:
        # Make sure server is up to date
        subprocess.Popen(['git', 'pull'], stdout=FNULL)
        # Make sure there are no local changes on server
        subprocess.Popen(['git', 'reset', '--hard'], stdout=FNULL)
        # Log the pull
        with open('logs/last_pull', 'w+') as pull_log:
            pull_log.write(str(datetime.now()))
        # Restart the server
        subprocess.Popen(['./manage.sh', 'restart'], stdout=FNULL)
    except Exception as exception:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Something went wrong!")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(exception))


if __name__ == "__main__":
    main()