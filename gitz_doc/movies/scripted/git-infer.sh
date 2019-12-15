# git-infer: Commit with an automatically generated message

touch one.txt
git add one.txt

git infer

echo one > one.txt
git infer
git infer -a
# -a means commit all changes
