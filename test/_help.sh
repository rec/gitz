python -m gitz.helper.main

if [ "" ] ; then
    for i in git-*; do
        echo '----------------------------------------------------------------'
        $i -h
    done
fi
echo '----------------------------------------------------------------'
