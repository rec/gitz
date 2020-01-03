# git-split: Split the staging area or the most recent commit
# into many individual commits

touch one.txt two.txt three.txt
git add one.txt two.txt three.txt
git commit -m BEGIN

echo ONE > one.txt
git rm two.txt
git mv three.txt four.txt
touch five.txt six.txt && git add five.txt

git split
git log --oneline
git reset --hard :/BEGIN
