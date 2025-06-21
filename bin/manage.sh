#!/bin/bash

set -e

COMMAND=$1
ENV_NAME=$2

if [ -z "$COMMAND" ] || [ -z "$ENV_NAME" ]; then
  echo "Usage: $0 {start|stop|restart|smoke} <env-name>"
  echo "Example: $0 start mars  (loads .env-mars)"
  exit 1
fi

ENV_FILE=".env-${ENV_NAME}"

if [ ! -f "$ENV_FILE" ]; then
  echo "Environment file '$ENV_FILE' not found."
  exit 1
fi

echo "Using environment: $ENV_FILE"

set -a
source "$ENV_FILE"
export HOST_UID=$(id -u)
export HOST_GID=$(id -g)
set +a

PORT="${DASH_PORT:-8050}"

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

  smoke)
    echo "Running smoke test against http://localhost:$PORT/overview ..."
    if ! curl -sf "http://localhost:$PORT/overview" > /dev/null; then
      echo "Smoke test failed: /overview did not respond with 200"
      exit 1
    fi
    echo "Smoke test passed!"
    ;;

  *)
    echo "Invalid command: $COMMAND"
    echo "Usage: $0 {start|stop|restart|smoke} <env-name>"
    exit 1
    ;;
esac