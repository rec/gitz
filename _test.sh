#!/usr/bin/env bash

set -Eeuo pipefail

FILES=`./_make_single_files list`

black -l 79 -S _gitz.py $FILES
flake8 _gitz.py $FILES
