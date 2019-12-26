# git-multi-pick - like git cherry-pick but for multiple commits

git new foo
touch one.txt && git add one.txt && git commit -m one
touch two.txt && git add two.txt && git commit -m two
touch three.txt && git add three.txt && git commit -m three
touch four.txt && git add four.txt && git commit -m four
touch five.txt && git add five.txt && git commit -m five
git log --oneline

git checkout master
git multi-pick foo~4 foo~2 foo
git log --oneline
