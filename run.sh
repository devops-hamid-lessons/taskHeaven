#!/usr/bin/env bash

set -o errexit
set -o pipefail

function show_usage {
  echo "Usage: run.sh --bind <ip:port> [-h]"
  echo "   "
  echo "  --bind         : ip and port to bind the service with. E.g. 0.0.0.0:2500"
  echo "  --help         : show this message and exit"
}

function parse_args {
  # Named args.
  while [[ "${1:-}" != "" ]]; do
    case "$1" in
    --bind)
      BIND="$2"
      shift
      ;;
    --help)
      show_usage
      exit
      ;;
    esac
    shift
  done
}


parse_args "$@"

# Validate required args.
if [[ -z "${BIND:-}" ]]; then
  echo "Invalid arguments."
  show_usage
  exit
fi


source ./venv/bin/activate
python3 -u main.py $BIND &
deactivate > /dev/null 2>&1
