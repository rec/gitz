#!/usr/bin/env bash

set -Eeo pipefail

FILES=`grep -l python3 git-* | xargs echo`

echo "Testing files $FILES"

flake8
flake8 $FILES
black -l 79 -S *.py test/*.py $FILES
export PATH=`pwd`:$PATH
pytest

for i in git-*; do
    echo '----------------------------------------------------------------'
    if [[ $i == git-open ]] ; then
        set +Ee
        $i -h
        set -Ee
    else
        $i -h
    fi
done
echo '----------------------------------------------------------------'
