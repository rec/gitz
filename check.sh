# FILES=git-combine git-loga git-logr git-rot git-snip git-split
FILES=`cat python_commands.txt`

flake8 _gitz.py $FILES
black -l 79 -S _gitz.py $FILES
