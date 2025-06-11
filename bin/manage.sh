#!/bin/bash

# Check if a command argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 {start|stop|restart}"
  exit 1
fi

COMMAND=$1

case "$COMMAND" in
  start)
    echo "Building the image and starting the container..."
    docker-compose build || { echo "Build failed"; exit 1; }
    docker-compose up -d || { echo "Failed to start container"; exit 1; }
    ;;
  stop)
    echo "Stopping and removing the container..."
    docker-compose down || { echo "Failed to stop container"; exit 1; }
    ;;
  restart)
    echo "Restarting the container..."
    docker-compose down || { echo "Failed to stop container"; exit 1; }
    docker-compose build || { echo "Build failed"; exit 1; }
    docker-compose up -d || { echo "Failed to start container"; exit 1; }
    ;;
  *)
    echo "Invalid command. Use start, stop, or restart."
    exit 1
    ;;
esac
