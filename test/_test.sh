#!/usr/bin/env bash

set -Eeo pipefail

python -m gitz_doc.get_command_summaries > gitz/program/summaries.py

./git-gitz c > test/gitz_commands.txt
FILES=`grep -l python3 git-* | xargs echo`

echo "Testing files $FILES"

black -l 79 -S *.py test/*.py gitz/*.py gitz_doc/*.py $FILES
flake8
flake8 $FILES
export PATH=`pwd`:$PATH
pytest $@
