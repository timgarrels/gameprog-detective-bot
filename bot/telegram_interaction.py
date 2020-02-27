"""Bot talking to a telegram user"""
import random
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import time

from bot import server_interaction as server

def send_delayed_message(message, chat_id, context, reply_keyboard=None):
    """Sends a message and an optional reply keyboard with realistic delay and return the Message object"""
    time.sleep(len(message) * 0.04)
    return context.bot.send_message(
        chat_id=chat_id,
        text=message,
        reply_markup=reply_keyboard)

def send_multiple_delayed_messages(messages, chat_id, context, reply_keyboard=None):
    """Sends multiple messages and an optional reply keyboard with realistic delay"""
    if reply_keyboard:
        if len(messages) == 0:
            return
        if len(messages) >= 2:
            send_delayed_message(messages.pop(0), chat_id, context, reply_keyboard=ReplyKeyboardMarkup([[" "]], True))
        last_message = messages.pop()
        for message in messages:
            send_delayed_message(message, chat_id, context)
        send_delayed_message(last_message, chat_id, context, reply_keyboard)
    else:
        for message in messages:
            send_delayed_message(message, chat_id, context, reply_keyboard=ReplyKeyboardRemove())

def delete_message(message, chat_id, context):
    """deletes a message from a user"""
    context.bot.delete_message(chat_id, message.message_id)

def flush_delete_queue(chat_id, context):
    """delete all the messages that have been added to the chat's delete queue and clear the queue"""
    delete_queue = context.chat_data.get("delete_queue")
    if delete_queue:
        for message in delete_queue:
            delete_message(message, chat_id, context)
        delete_queue.clear()

def get_reply_keyboard(user_handle):
    """Creates a reply keyboard from the users current answer options (fetched from server)"""
    reply_options = server.get_user_reply_options(user_handle)

    reply_keyboard = None
    if reply_options:
        reply_keyboard = ReplyKeyboardMarkup([[reply_option] for reply_option in reply_options], True)
    return reply_keyboard

def send_current_description(update, context):
    """sends the current story point description and corresponding user replies"""
    user_handle = update.effective_user.username
    messages = server.get_current_story_description(user_handle)
    reply_keyboard = get_reply_keyboard(user_handle)
    send_multiple_delayed_messages(messages, update.effective_chat.id, context, reply_keyboard)

def reply(update, context, filler=True):
    """Proceeds the user in the story. Replies to message send by the player with API provided
    answers and displays new buttons"""
    user_handle = update.effective_user.username
    chat_id = update.effective_chat.id
    user_reply = update.message

    server_response = server.proceed_story(user_handle, user_reply)
    if server_response:
        if not server_response["validReply"]:
            delete_queue = context.chat_data.setdefault("delete_queue", [])
            delete_queue.append(user_reply)
            message = "Benutze die vorgegebenen Buttons"
            reply_keyboard = get_reply_keyboard(user_handle)
            delete_queue.append(send_delayed_message(message, chat_id, context, reply_keyboard))
        else:
            flush_delete_queue(chat_id, context)
            messages = server_response["newMessages"]
            reply_keyboard = get_reply_keyboard(user_handle)
            send_multiple_delayed_messages(messages, chat_id, context, reply_keyboard)

# --------- Register handshake ---------
def start_command_callback(update, context):
    """ Provides logic to handle a newly started chat with a user """
    user = update.effective_user
    user_handle = user.username

    if server.user_already_registered(user_handle):
        send_current_description(update, context)
    else:
        try:
            auth_key = context.args[0]
            valid, response_text = server.try_to_register_user(auth_key, user_handle, user.first_name)
            if valid:
                messages = server.get_current_story_description(user_handle)
            else:
                messages = ["Ich kenne dich nicht...", "Ich spreche nicht mit Fremden", f"Server Response: {response_text}"]
        except IndexError:
            # No Auth key
            messages = ["Wer bist du?", "<no token>"]
        
        reply_keyboard = get_reply_keyboard(user_handle)
        send_multiple_delayed_messages(messages, update.effective_chat.id, context, reply_keyboard)
