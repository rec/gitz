#!/usr/bin/env bash

set -Eeo pipefail

FILES=`grep -l python3 git-* | xargs echo`

echo "Testing files $FILES"

flake8
flake8 $FILES
export PATH=`pwd`:$PATH
python3.5 -m unittest discover -p \*_test.py
