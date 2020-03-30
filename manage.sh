#! /usr/bin/env bash

command=$1

# switch to parent folder of this script
cd $(dirname $0)

if [ "$command" == "install" ]; then
    if [ ! -d logs ]; then
        echo "Creating logs directory"
        mkdir -p logs
    fi
    if [ ! -d .venv ]; then
        echo "Creating virual environment"
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    set_env=true
    if [ -f env_vars ]; then
        read -p "server URL and bot token already set - reset them? (y/n): " reset_env
        if [ $reset_env != "y" ]; then set_env=false; fi
    fi
    if $set_env; then
        echo "==========================================================================="
        read -p "Please enter the IP adress of the server (defaults to localhost): " server_ip
        read -p "Please enter the token of your bot (received from the telegram bot father): " bot_token
        echo "==========================================================================="
        server_url="http://$([ -z $server_ip ] && echo localhost || echo $server_ip):8080"
        echo "export GP_SERVER_URL=$server_url" > env_vars
        echo "export GP_TELEGRAM_BOT_TOKEN=$bot_token" >> env_vars
    fi
    exit
fi

# try to load venv
if [ -d .venv ]; then
    source .venv/bin/activate
else
    echo "please first install the bot"
    exit
fi
[ -f env_vars ] && source env_vars

if [ "$command" == "start" ]; then
    if [ -f logs/bot_pid ] && ps -p `cat logs/bot_pid` > /dev/null; then
        echo "bot already running"
        exit
    fi
    echo "Starting bot..."
    echo "----------" >> logs/bot_log
    python bot.py >> logs/bot_log 2>&1 &
    echo $! > logs/bot_pid
elif [ "$command" == "kill" ]; then
    if [ -f logs/bot_pid ] && ps -p `cat logs/bot_pid` > /dev/null; then
        echo "Killing running bot..."
        kill -9 `cat logs/bot_pid`
    else
        echo "Bot not running"
    fi
elif [ "$command" == "restart" ]; then
    ./manage.sh kill
    ./manage.sh start
elif [ "$command" == "log" ]; then
    less -r +F logs/bot_log
elif [ "$command" == "help" ] || [ "$command" == "" ]; then
    echo "Usage: ./manage.sh [command]"
    echo ""
    echo "Available commands:"
    echo "./manage.sh install - Install and Setup Bot"
    echo "./manage.sh start - Start new Bot instance"
    echo "./manage.sh kill - Kill running Bot instance"
    echo "./manage.sh restart - Kill running Bot instance and start a new one"
    echo "./manage.sh log - Show Bot logs"
    echo "./manage.sh help - Display this text"
else
    echo "Unkown command, use ./manage.sh help to view available commands"
fi
