#!/bin/bash

set -e

COMMAND=$1

if [ -z "$COMMAND" ]; then
  echo "Usage: $0 {start|stop|restart}"
  exit 1
fi

case "$COMMAND" in
  start)
    echo "Building and starting the container..."
    docker compose build
    docker compose up -d
    ;;
  stop)
    echo "Stopping and removing the container..."
    docker compose down
    ;;
  restart)
    echo "Restarting the container..."
    docker compose down
    docker compose build
    docker compose up -d
    ;;
  *)
    echo "Invalid command: $COMMAND"
    echo "Usage: $0 {start|stop|restart}"
    exit 1
    ;;
esac
