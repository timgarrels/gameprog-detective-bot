"""Bot talking to a telegram user"""
import random
from telegram import ReplyKeyboardMarkup, KeyboardButton
import time

from bot import server_interaction as server


def send_delayed_message(message, chat_id, context, reply_keyboard=None):
    """Sends a message and an optional reply keyboard with realistic delay"""
    time.sleep(len(message) * 0.04)
    context.bot.send_message(
        chat_id=chat_id,
        text=message,
        reply_markup=reply_keyboard)

def send_delayed_messages(messages, chat_id, context, reply_keyboard=None):
    """Sends multiple messages and an optional reply keyboard with realistic delay"""
    if reply_keyboard:
        # All messages require a text, even the reply markups. So reserve one answer for that markup
        last_message = messages.pop()
        for message in messages:
            send_delayed_message(message, chat_id, context)
        send_delayed_message(last_message, chat_id, context, reply_keyboard)
    else:
        for message in messages:
            send_delayed_message(message, chat_id, context)

def send_filler(update, context):
    """We need to remove the old repy keyboard.
    Telegram API does not allow us to replace the keyboard with an empty one
    without a message send. Removing (not replacing) the keyboard would be possible,
    but makes the screen of the user jump up and down.
    This function chooses a filler like "I see" from a list (which should
    contain a lot of __small__ filler statements) and sends
    an empty keyboard to remove old keyboard"""
    # TODO: This is a hacky solution, but I did not find a better one
    # after exploring OneTimeKeyboards
    # Needs further discussion
    # Tim Garrels, 23_Nov_2019
    filler = random.choice(["I see", "If you say so", "Mh", "Ah"])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=filler, reply_markup=ReplyKeyboardMarkup([[KeyboardButton(" ")]]))

# ---------- Communication ----------
def get_reply_keyboard(user_handle):
    """Creates a reply keyboard from the users current answer options (fetched from server)"""
    reply_options = server.get_user_reply_options(user_handle)

    reply_keyboard = None
    if reply_options:
        reply_keyboard = ReplyKeyboardMarkup([
            [KeyboardButton(reply_option) for reply_option in reply_options]
        ])
    return reply_keyboard

def send_current_description(update, context):
    """sends the current story point description and corresponding user replies"""
    user_handle = update.effective_user.username
    messages = server.get_current_story_description(user_handle)
    reply_keyboard = get_reply_keyboard(user_handle)
    send_delayed_messages(messages, update.effective_chat.id, context, reply_keyboard)

def reply(update, context, filler=True):
    """Proceeds the user in the story. Replies to message send by the player with API provided
    answers and displays new buttons"""
    user_handle = update.effective_user.username
    chat_id = update.effective_chat.id
    user_reply = update.message

    server_response = server.proceed_story(user_handle, user_reply)
    if server_response:
        # TODO: remove filler once bot can delete invalid user replies
        if filler:
            send_filler(update, context)

        if not server_response["validReply"]:
            # TODO: delete message
            pass
        else:
            messages = server_response["newMessages"]
            reply_keyboard = get_reply_keyboard(user_handle)
            send_delayed_messages(messages, chat_id, context, reply_keyboard)

# --------- Register handshake ---------
def start_command_callback(update, context):
    """ Provides logic to handle a newly started chat with a user """
    user = update.effective_user
    user_handle = user.username

    # TODO: What does this do?
    # Nothing should happen if a user types "\start" if he is already registered
    if not server.user_already_registered(user_handle):
        try:
            auth_key = context.args[0]
            valid, response_text = server.try_to_register_user(auth_key, user_handle, user.first_name)
            if valid:
                messages = server.get_messages(user_handle)
            else:
                messages = ["I don't know you!", "I don't speak to strangers", f"Server Response: {response_text}"]
        except IndexError:
            # No Auth key
            messages = ["Who are you?", "I don't speak to people who don't introduce themselves!", "<no token>"]
        
        reply_keyboard = get_reply_keyboard(user_handle)
        send_delayed_messages(messages, update.effective_chat.id, context, reply_keyboard)
