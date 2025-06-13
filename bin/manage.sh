#!/bin/bash

set -e

COMMAND=$1
ENV_NAME=$2

if [ -z "$COMMAND" ] || [ -z "$ENV_NAME" ]; then
  echo "Usage: $0 {start|stop|restart} <env-name>"
  echo "Example: $0 start mars  (loads .env-mars)"
  exit 1
fi

ENV_FILE=".env-${ENV_NAME}"

if [ ! -f "$ENV_FILE" ]; then
  echo "Environment file '$ENV_FILE' not found."
  exit 1
fi

echo "Using environment: $ENV_FILE"

# Export env vars for docker compose build
set -a
source "$ENV_FILE"
set +a

case "$COMMAND" in
  start)
    echo "Building and starting the container (no cache)..."
    docker compose build --no-cache
    docker compose --env-file "$ENV_FILE" up -d
    ;;
  stop)
    echo "Stopping and removing the container..."
    docker compose down
    ;;
  restart)
    echo "Restarting the container (no cache)..."
    docker compose down
    docker compose build --no-cache
    docker compose --env-file "$ENV_FILE" up -d
    ;;
  *)
    echo "Invalid command: $COMMAND"
    echo "Usage: $0 {start|stop|restart} <env-name>"
    exit 1
    ;;
esac
