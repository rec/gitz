#!/usr/bin/env bash

set -Eeuo pipefail

FILES=`python3 single_file/_single_file.py list`

black -l 79 -S _gitz.py $FILES
flake8 _gitz.py $FILES
