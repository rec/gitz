# git-update - rebase and force-push all working branches from upstream

git new one
touch one.txt && git add one.txt && git commit -m one && git push

git new two
touch two.txt && git add two.txt && git commit -m two && git push

git checkout master
touch zero.txt && git add zero.txt && git commit -m zero && git push

git update
git for-each - git log --oneline
