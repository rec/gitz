# git-shuffle: reorder recent commits

touch one.txt
git add one.txt
git infer
touch two.txt
git add two.txt
git infer
touch three.txt
git add three.txt
git infer
git log --oneline

git shuffle ba
git log --oneline

git shuffle ba
git log --oneline
# Back to normal

touch four.txt
git add four.txt
git infer
touch five.txt
git add five.txt
git infer
git log --oneline

git shuffle bcead
git log --oneline
git shuffle bcead
git shuffle bcead
git shuffle bcead
git shuffle bcead

git log --oneline
# Back to normal

# Delete and shuffle
git shuffle _ba
git log --oneline

git shuffle abcd -s "A new commit"
git show
