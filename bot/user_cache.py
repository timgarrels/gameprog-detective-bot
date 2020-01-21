import requests
from json.decoder import JSONDecodeError

from bot import LOGGER, SERVER_URL

class UserIdCache(dict):
    def __missing__(self, handle):
        api_url = SERVER_URL + "/users?handle={handle}"
        response = requests.get(api_url.format(handle=handle))
        if response.status_code == 200:
            self[handle] = response.json()["userId"]
            return self[handle]
        debug_message = "Server Side lookup of {handle} failed: {response}"
        LOGGER.debug(debug_message.format(handle=handle, response=response))

user_id_cache = UserIdCache()