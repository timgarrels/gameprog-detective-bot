"""Bot asking server for guidance"""

import requests

from bot import LOGGER, SERVER_URL
from bot.user_cache import user_id_cache

# --------- Uitility ---------
def get_answers(handle, message):
    """This is the first main part of the bot.
    It asks the server for an answer depending on a telegram user and a send message"""
    api_url = SERVER_URL + "/users/{id}/story/proceed?reply={reply}"
    LOGGER.error("GETANSWERS HANDLE: {}".format(handle))
    user_id = user_id_cache[handle]

    LOGGER.error("This id was send")
    LOGGER.error(user_id)
    response = requests.get(api_url.format(id=user_id, reply=message.text))
    if response.status_code == 200:
        return response.json()

    debug_message = """The Server did not provide answers for \
id '{id}' and message '{message}'"""
    LOGGER.debug(debug_message.format(id=user_id, message=message.text))
    LOGGER.debug("Server Reply: {}".format(response.text))
    return []

def get_new_user_reply_options(handle):
    """This is the second main part of the bot.
    It asks the server for replys depending on a telegram user.
    As the server knows the gamestate of that user it can provide individual replys"""

    api_url = SERVER_URL + "/users/{id}/story/user-replies"
    LOGGER.error("GETREPLYOPTIONS HANDLE: {}".format(handle))
    user_id = user_id_cache[handle]

    response = requests.get(api_url.format(id=user_id))
    if response.status_code == 200:
        return response.json()
    LOGGER.debug("The Server did not provide reply options for id {id}".format(
        id=user_id))
    return []

def user_already_registerd(telegram_handle):
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
