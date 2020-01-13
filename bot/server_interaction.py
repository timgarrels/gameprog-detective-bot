"""Bot asking server for guidance"""

import requests

from bot import LOGGER, SERVER_URL

# --------- Uitility ---------
def get_answers(user, message):
    """This is the first main part of the bot.
    It asks the server for an answer depending on a telegram user and a send message"""
    api_url = SERVER_URL + """/user/answersForUserAndReply?\
telegramUser={username}&reply={reply}"""
    response = requests.get(api_url.format(username=user.username, reply=message.text))
    if response.status_code == 200:
        return response.json()

    debug_message = """The Server did not provide answers for \
username '{username}' and message '{message}'"""
    LOGGER.debug(debug_message.format(username=user.username, message=message.text))
    LOGGER.debug("Server Reply: {}".format(response.text))
    return []

def get_new_user_reply_options(user):
    """This is the second main part of the bot.
    It asks the server for replys depending on a telegram user.
    As the server knows the gamestate of that user it can provide individual replys"""

    api_url = SERVER_URL + "/user/replyOptionsForUser?telegramUser={username}"
    response = requests.get(api_url.format(username=user.username))
    if response.status_code == 200:
        return response.json()
    LOGGER.debug("The Server did not provide reply options for username {username}".format(
        username=user.username))
    return []

def user_already_registerd(telegram_handle):
    """Check whether a telegram user is already playing"""
    api_url = SERVER_URL + "/user/byTelegramHandle?telegramHandle={}"
    response = requests.get(api_url.format(telegram_handle))
    if response.status_code == 200:
        return True
    return False

def try_to_register_user(start_token, user_handle, user_first_name):
    """ Calls register API endpoint to register the handle that provided a token.
    Returns True and response text if the register process was successfull (status 200),
    False and response text otherwise"""
    api_url = SERVER_URL + "/user/register?\
telegramHandle={handle}&userFirstName={firstName}&telegramStartToken={token}"
    response = requests.get(api_url.format(handle=user_handle, firstName=user_first_name, token=start_token))
    if response.status_code == 200:
        return True, response.text
    if response.status_code == 500:
        return False, "Internal Server Error"
    return False, response.text
