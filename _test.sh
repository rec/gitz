#!/usr/bin/env bash

set -Eeuo pipefail

FILES=`grep -l python3 git-* | xargs echo`

echo "Testing files $FILES"

black -l 79 -S _gitz.py $FILES
flake8 _gitz.py $FILES
