# git-save - save the entire state of absolutely everything.

touch one.txt && git add one.txt && git commit -m one
touch two.txt && git add two.txt && git commit -m two
touch three.txt && git add three.txt && git commit -m three

echo ONE > one.txt
git rm two.txt
git mv three.txt four.txt
echo FIVE > five.txt
git add five.txt
touch six.txt

git st
git save -a
git reset --hard :/one
ls
git save pop
