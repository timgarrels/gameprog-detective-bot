import logging
import os

_SERVER_URL_ENV_VAR = "GP_SERVER_URL"
try:
    SERVER_URL = os.environ[_SERVER_URL_ENV_VAR]
except KeyError:
    print("You did not set {}".format(_SERVER_URL_ENV_VAR))
    exit()

_BOT_TOKEN_ENV_VAR = "GP_TELEGRAM_BOT_TOKEN"
try:
    BOT_TOKEN = os.environ[_BOT_TOKEN_ENV_VAR]
except KeyError:
    print("You did not set {}".format(_BOT_TOKEN_ENV_VAR))
    exit()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)
