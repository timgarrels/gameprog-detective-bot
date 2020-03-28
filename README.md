# gameprog-detective-bot

Dies ist der `bot` Teil des Gameprog Projektes von Antonio Dimeo, Tim Garrels, Paul Methfessel und Robin Wersich.
Eine umfassende README ist im repository des [servers](https://github.com/EatingBacon/gameprog-detective-server) zu finden.

## Install and Start
Voraussetzung ist ein installiertes Python 3
1. `./manage.sh install` um den bot zu installieren
1. `./manage.sh start` um den bot zu starten
1. für weitere befehle `./manage.sh help` benutzen

## About
Dieser Bot benutzt den [python-telegram-bot wrapper](https://python-telegram-bot.org/). `bot.py` registriert einen `/start` und einen `/describe` Befehl und einen `text-handler`:  
- `/start` - Registrierungs Befehl durch die [App](https://github.com/ADimeo/gameprog-detective-app) um `telegramHandle` mit `userId` zu verbinden
- `/describe` - Lässt den Bot die Beschreibung des aktuellen [storypoint](https://github.com/EatingBacon/gameprog-detective-server/wiki/Story-Storypoint) senden
- `text-handler` - Hauptkomponente des Bots, um die Story weiterzuführen

## Config
- Dieser Bot benötigt einen [server](https://github.com/EatingBacon/gameprog-detective-server) um zu funktionieren. Die IP des servers muss während des Installationsprozesses eingegeben werden
- Dieser Bot benötigt ein [telegram-bot-token](https://core.telegram.org/bots#6-botfather). Auch dieses muss während der Installation eingegeben werden.
