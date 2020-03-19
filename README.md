# gameprog-detective-bot

This is the `bot` part of the Gameprog Project of Antonio Dimeo, Tim Garrels, Paul Methfessel and Robin Wersich.

## Install and Start
It is recommended to use a virtual environment
``` bash
virtualenv --python=python3 .venv
source .venv/bin/activate
```

- Use `./manage.sh install` to install and setup the bot
- Use `./manage.sh start` to start the bot
- For more commands use `./manage.sh help`

## About
This bot uses the [python-telegram-bot wrapper](https://python-telegram-bot.org/). `bot.py` registeres a `/start` and a `/describe` command and a `text-handler`:  
`/start` - Register command provided by the [app](https://github.com/ADimeo/gameprog-detective-app) to associate `telegramHandle` with `userId`  
`/describe` - Prints description of current [storypoint](https://github.com/EatingBacon/gameprog-detective-server/wiki/Story-Storypoint)  
`text-handler` - Main part of the bot, used to proceed in the story (main interaction)

`bot/server_interaction.py` wraps important API calls to the [server](https://github.com/EatingBacon/gameprog-detective-server) into function calls.  
`bot/telegram_interaction.py` handles chat interaction with the player by interpreting and answering messages.
