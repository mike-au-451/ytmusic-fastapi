#!/bin/bash

# APPDIR=/home/mike/Play/2024/01/20240125_01/app
APPDIR="$1"

if [[ ! -d $APPDIR ]]
then
	mkdir -p $APPDIR
fi
if [[ $? -ne 0 ]]
then
	echo "FATAL: failed to create ${APPDIR:-APPDIR}"
	echo "USAGE: setup.sh APPDIR"
	exit
fi

set -e

cd $APPDIR

# Set up the python environment and install dependencies.

if [[ ! -f pyvenv.cfg ]]
then
	# Create a python virtual environment
	python3 -m venv .
fi
source bin/activate

pip install fastapi jinja2 ytmusicapi uvicorn

echo source bin/activate
