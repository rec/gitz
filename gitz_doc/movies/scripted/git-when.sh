# git-when: When were things changed?

cd /code/gitz
touch one.txt && git add one.txt && git commit -m one
sleep 1
touch two.txt && git add two.txt && git commit -m two
touch three.txt four.txt && git add three.txt

git when
