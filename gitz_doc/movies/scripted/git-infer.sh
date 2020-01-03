# git-infer: Commit with an automatically generated message

touch one.txt && git add one.txt
git infer

# -a means commit all changes
echo one > one.txt
git infer
git infer -a
