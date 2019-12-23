# git-st: Colorful, compact git status command

touch one.txt two.txt three.txt && git add one.txt two.txt three.txt
git commit -m BEGIN

echo ONE > one.txt
git rm two.txt
git mv three.txt four.txt
echo FIVE > five.txt
git add five.txt
touch six.txt

git st
