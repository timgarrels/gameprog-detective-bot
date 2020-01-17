import requests
from json.decoder import JSONDecodeError

from bot import SERVER_URL


class UserCache():
    association = {}

    def get(handle):
        if UserCache.association.get(handle, None):
            # Handle in Cache
            return UserCache.association[handle]
        else:
            # Handle not in Cache
            UserCache.association[handle] = UserCache._get_user_id_by_handle(handle)
            return UserCache.association[handle]

    def _get_user_id_by_handle(handle):
        api_url = SERVER_URL + "/users?handle={handle}"
        response = requests.get(api_url.format(handle=handle))
        if response.status_code == 200:
            return response.json()["user_id"]
        debug_message = "Server Side lookup of {handle} failed: {reponse}"
    LOGGER.debug(debug_message.format(handle=handle, response=response))