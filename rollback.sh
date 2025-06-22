#!/bin/bash
# rollback.sh <timestamp> <env>
set -e
RELEASES_DIR="/apps/data/dashboard/releases"
LINK_PATH="/apps/data/dashboard/current"

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <timestamp> <env-name>"
  exit 1
fi

RELEASE="$RELEASES_DIR/$1"

if [ ! -d "$RELEASE" ]; then
  echo "Release $RELEASE does not exist."
  exit 1
fi

ln -sfn "$RELEASE" "$LINK_PATH"
cd "$LINK_PATH"
bash bin/manage.sh restart "$2"