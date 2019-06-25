# FILES=git-combine git-loga git-logr git-rot git-snip git-split
FILES=`cat python-files.txt`

flake8 $FILES
black -l 79 -S $FILES
