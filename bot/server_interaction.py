"""Bot asking server for guidance"""

import requests

from bot import LOGGER, SERVER_URL
from bot.user_cache import user_id_cache

# --------- Uitility ---------
def send_user_reply(handle, message):
    """Sends a user reply to the server and
    returns the server response on success (None otherwise)"""
    api_url = SERVER_URL + "/users/{id}/story/proceed?reply={reply}"
    user_id = user_id_cache[handle]
    LOGGER.debug(f"SEND REPLY HANDLE: {handle}")

    response = requests.get(api_url.format(id=user_id, reply=message.text))

    if response.status_code == 200:
        return response.json()
    else:
        LOGGER.error(f"There was an error while proceeding the story for user {user_id} and message {message.text}")
        LOGGER.error(f"Server Reply: {response.text}")
        return None

def get_messages(handle):
    """asks the server for messages for a telegram user and returns it"""
    api_url = SERVER_URL + "/users/{id}/story/bot-messages"
    user_id = user_id_cache[handle]
    LOGGER.debug(f"GET MESSAGES HANDLE: {handle}")

    response = requests.get(api_url.format(id=user_id))
    if response.status_code == 200:
        return response.json()
    else:
        LOGGER.error(f"The server did not provide messages for user {user_id}")
        LOGGER.error(f"Server Reply: {response.text}")
        return []

def get_user_reply_options(handle):
    """asks the server for reply options for a telegram user and returns them"""
    api_url = SERVER_URL + "/users/{id}/story/user-replies"
    user_id = user_id_cache[handle]
    LOGGER.debug(f"GET REPLY OPTIONS HANDLE: {handle}")

    response = requests.get(api_url.format(id=user_id))
    if response.status_code == 200:
        return response.json()
    else:
        LOGGER.debug(f"The Server did not provide reply options for user {user_id}")
        return []

def user_already_registered(telegram_handle):
    """Check whether a telegram user is already playing"""
    api_url = SERVER_URL + "/users?handle={}"
    response = requests.get(api_url.format(telegram_handle))
    if response.status_code == 200:
        return True
    return False

def try_to_register_user(start_token, user_handle, user_first_name):
    """ Calls register API endpoint to register the handle that provided a token.
    Returns True and response text if the register process was successfull (status 200),
    False and response text otherwise"""
    api_url = SERVER_URL + "/users/register?\
handle={handle}&firstname={firstname}&token={token}"
    response = requests.get(api_url.format(handle=user_handle, firstname=user_first_name, token=start_token))
    if response.status_code == 200:
        return True, response.text
    if response.status_code == 500:
        return False, "Internal Server Error"
    return False, response.text
