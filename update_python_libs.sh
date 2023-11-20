#!/bin/zsh

clear; pip list --outdated
pip install --upgrade pip setuptools wheel
pip install --upgrade --upgrade-strategy eager -r requirements.txt
pip freeze > requirements.lock
pipenv update
git add Pipfile.lock requirements.lock
