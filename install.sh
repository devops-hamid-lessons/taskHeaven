#!/usr/bin/env bash

set -o pipefail

function exit_if_failed()
{
  if [[ "$1" -ne 0 ]]; then
    echo "$2"
    exit 1;
  fi
}

# Check if user is root
if [[ $EUID -ne 0 ]] ; then echo "Please run as a superuser." ; exit 1 ; fi

echo "Update repository..."

apt-get update -y
if [[ $? -ne 0 ]]; then
  apt-get --fix-broken install -y
  apt-get update -y
  exit_if_failed $? "Error: Unable to update repository"
fi

echo "Install required packages..."

apt-get install python3 -y
exit_if_failed $? "Error: Unable to install python3"

apt-get -y install python3-pip python3-venv python3-dev
if [[ $? -ne 0 ]]; then
  apt-get --fix-broken install -y
  apt-get -y install python3-pip python3-venv python3-dev
  exit_if_failed $? "Error: Unable to install pip, venv, and dev."
fi

echo "Create Python virtual environment..."

# Create environment as non root
sudo -u $SUDO_USER python3 -m venv venv
exit_if_failed $? "Error: Unable to create venv."

source venv/bin/activate
exit_if_failed $? "Error: Unable to activate venv."

echo "Install python packages..."

pip3 install --default-timeout=100 -r requirements.txt
exit_if_failed $? "Error: Unable to install requirements."

deactivate

chmod +x run.sh > /dev/null 2>&1
#exit_if_failed $? "Error: Unable to do <chmod +x run.sh>."

echo "*************************Installation completed.*******************************"