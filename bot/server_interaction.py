"""Bot asking server for guidance"""

import requests

from bot import LOGGER, SERVER_URL
from bot.user_cache import user_id_cache

# --------- Uitility ---------
def proceed_story(handle, user_reply):
    """Sends a user reply to the server and
    returns the server response on success (None otherwise)"""
    api_url = SERVER_URL + "/users/{id}/story/proceed?reply={reply}"
    user_id = user_id_cache[handle]
    if user_id:
        response = requests.post(api_url.format(id=user_id, reply=user_reply.text))
        if response.status_code == 200:
            return response.json()
        LOGGER.error(f"There was an error while proceeding the story for user {user_id} and user reply {user_reply.text}")
        LOGGER.error(f"Server Reply: {response.text}")
    return None

def get_current_story_description(handle):
    """asks the server for messages for a telegram user and returns it"""
    api_url = SERVER_URL + "/users/{id}/story/current-story-point/description"
    user_id = user_id_cache[handle]
    if user_id:
        response = requests.get(api_url.format(id=user_id))
        if response.status_code == 200:
            return response.json()
        LOGGER.error(f"The server did not provide a story description for user {user_id}")
        LOGGER.error(f"Server Reply: {response.text}")
    return []

def get_user_reply_options(handle):
    """asks the server for reply options for a telegram user and returns them"""
    api_url = SERVER_URL + "/users/{id}/story/current-story-point/user-replies"
    user_id = user_id_cache[handle]
    if user_id:
        response = requests.get(api_url.format(id=user_id))
        if response.status_code == 200:
            return response.json()
        LOGGER.error(f"The Server did not provide reply options for user {user_id}")
        LOGGER.error(f"Server Reply: {response.text}")
    return []

def reset_user(handle):
    """if a user with the given user already exists, reset it"""
    user_id_cache.pop(handle, "")
    response = requests.get(SERVER_URL + f"/users?handle={handle}")
    if response.status_code == 200:
        user_id = response.json()["userId"]
        requests.patch(SERVER_URL + f"/users/{user_id}/reset")

def try_to_register_user(start_token, user_handle, user_first_name):
    """ Calls register API endpoint to register the handle that provided a token.
    Returns True and response text if the register process was successfull (status 200),
    False and response text otherwise"""
    api_url = SERVER_URL + "/users/register?\
handle={handle}&firstname={firstname}&token={token}"
    response = requests.patch(api_url.format(handle=user_handle, firstname=user_first_name, token=start_token))
    if response.status_code == 200:
        return True, response.text
    if response.status_code == 500:
        return False, "Internal Server Error"
    return False, response.text
