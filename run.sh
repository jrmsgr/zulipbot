#!/bin/bash

cd "$(dirname "$0")"
PYTHON=./venv/bin/python
[ -x "$PYTHON" ] || PYTHON=python3
(nohup "$PYTHON" -u main.py > out.log 2>&1)&
