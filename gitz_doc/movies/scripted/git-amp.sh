# git-amp: AMend and force Push!

touch 1.txt
git add 1.txt
git commit -am "Add 2.txt"
git push
git log --oneline
# oops!

git amp Add 1.txt
git log --oneline

# Fixed and force-pushed
