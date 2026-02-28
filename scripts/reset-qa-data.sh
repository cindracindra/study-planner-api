#!/usr/bin/env bash
set -euo pipefail # Force stop on any failure

YEAR="$1"

if [[ -z "$YEAR" ]]; then
  echo "ERROR: Year argument is required"
  echo "Usage: $0 2526"
  exit 1
fi

docker exec $(docker ps -qf "name=study-planner-api_web" | head -n1) bash -c "python cli.py erase_data --force && python cli.py populate_db ${YEAR}"
