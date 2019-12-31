#! /usr/bin/env bash

command=$1

if [ "$command" == "install" ]; then
    if [ ! -d logs ]; then
        echo "Creating logs directory"
        mkdir -p logs
    fi

    pip install -r requirements.txt
elif [ "$command" == "start" ]; then
    echo "Starting bot..."
    echo "----------" >> logs/bot_log
    python3 bot.py >> logs/bot_log 2>&1 &
    echo $! > logs/bot_pid
    echo "For logs use cat logs/bot_log"
elif [ "$command" == "kill" ]; then
    if ps -p `cat logs/bot_pid` > /dev/null; then
        echo "Killing running bot..."
        kill -9 `cat logs/bot_pid`
    else
        echo "Bot not running"
    fi
elif [ "$command" == "restart" ]; then
    `./manage.sh kill`
    `./manage.sh start`
elif [ "$command" == "help" ] || [ "$command" == "" ]; then
    echo "Usage: ./manage.sh [command]"
    echo ""
    echo "Available commands:"
    echo "./manage.sh install - Install and Setup Bot"
    echo "./manage.sh start - Start new Bot instance"
    echo "./manage.sh kill - Kill running Bot instance"
    echo "./manage.sh restart - Kill running Bot instance and start a new one"
    echo "./manage.sh help - Display this text"
else
    echo "Unkown command, use ./manage.sh help to view available commands"
fi
