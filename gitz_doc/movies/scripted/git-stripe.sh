# git-stripe: Create upstream branches for commit IDs in history
# to convince CI to re-compile them.

touch one.txt && git add one.txt && git commit -m one
touch two.txt && git add two.txt && git commit -m two
touch three.txt && git add three.txt && git commit -m three
touch four.txt && git add four.txt && git commit -m four

git stripe
git branch -a
git stripe --count 3
git branch -a
git stripe -d
git branch -a
