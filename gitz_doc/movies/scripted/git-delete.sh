# git-delete: Delete branches, both locally and remotely

git new one two three
git branch -a

git delete one two
git branch -a

# You need the --protected flag to overwrite protected branches
git new --protected develop
git branch -a

git delete develop
git delete --protected develop
git branch -a
