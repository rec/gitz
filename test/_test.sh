#!/usr/bin/env bash

set -Eeo pipefail

./git-gitz c > test/gitz_commands.txt
FILES=`grep -l python3 git-* | xargs echo`

echo "Testing files $FILES"

black -l 79 -S *.py test/*.py $FILES
flake8
flake8 $FILES
export PATH=`pwd`:$PATH
pytest $@
