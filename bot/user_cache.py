import requests
from json.decoder import JSONDecodeError

from bot import LOGGER, SERVER_URL

class UserIdCache(dict):
    """Caches telegramHandle - userId relations"""
    def __missing__(self, handle):
        """Updates cache on missing userId by making a server request"""
        api_url = SERVER_URL + "/users?handle={handle}"
        response = requests.get(api_url.format(handle=handle))
        if response.status_code != 200:
            debug_message = "Server Side lookup of {handle} failed: {response}"
            LOGGER.error(debug_message.format(handle=handle, response=response))
            return None
        self[handle] = response.json()["userId"]
        return self[handle]

user_id_cache = UserIdCache()